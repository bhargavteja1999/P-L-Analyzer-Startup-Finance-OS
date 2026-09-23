const MONTHS=["January","February","March","April","May","June","July","August","September","October","November","December"];
const STORAGE_KEY="pnl_v2";
const API_BASE="http://localhost:5000";
let DATA_MODE=localStorage.getItem("pnl_mode")||"local"; // local | sql | mongo
let CURRENT_BIZ=parseInt(localStorage.getItem("current_biz")||"1"); // define early to avoid TDZ
console.log("P&L Analyzer v=mongo3 DATA_MODE=",DATA_MODE,"CURRENT_BIZ",CURRENT_BIZ); // debug: proves mongo code loaded
let DISPLAY_FMT=localStorage.getItem("display_fmt")||"lakh"; // lakh | full
const fmt=n=>{
  const num=Number(n);
  if(DISPLAY_FMT==="lakh"){
    if(num>=1e7) return "₹"+(num/1e7).toFixed(2)+" Cr";
    if(num>=1e5) return "₹"+(num/1e5).toFixed(2)+" L";
  }
  return "₹"+num.toLocaleString("en-IN",{minimumFractionDigits:2,maximumFractionDigits:2});
};
const fmt0=n=>{
  const num=Number(n);
  if(DISPLAY_FMT==="lakh"){
    if(num>=1e7) return "₹"+(num/1e7).toFixed(2)+" Cr";
    if(num>=1e5) return "₹"+(num/1e5).toFixed(2)+" L";
  }
  return "₹"+num.toLocaleString("en-IN");
};
// PDF-safe formatter — jsPDF's built-in Helvetica does NOT support U+20B9 (₹) so it renders as garbled "'1".
// Use ASCII "Rs. " for PDF export to keep numbers clear.
const fmtPdf=n=>"Rs. "+Number(n).toLocaleString("en-IN",{minimumFractionDigits:2,maximumFractionDigits:2});
const fmtPdf0=n=>"Rs. "+Number(n).toLocaleString("en-IN");

// ===== Input helpers — Show Lakhs / Crores when >= ₹1,00,000 (above 99999) =====
function cleanNumberString(s){ return String(s).replace(/[,₹\s]/g,'').trim(); }
function parseLakhCrore(s){
  const t=String(s).trim();
  // Match "1.5 L", "1.5L", "1.5 Cr", "1.5Cr", case-insensitive
  const m=t.match(/^([0-9,.]+)\s*([lL]|[cC][rR])\b/);
  if(m){
    const num=parseFloat(m[1].replace(/,/g,''));
    if(isNaN(num)) return NaN;
    const unit=m[2].toLowerCase();
    if(unit==='l') return num*1e5;
    if(unit==='cr') return num*1e7;
  }
  return NaN;
}
function toNumber(s){
  const sStr=String(s).trim();
  if(sStr===""||sStr==="-") return NaN;
  // First try L/Cr parsing (e.g., "1.00 L" -> 100000)
  const lakhVal=parseLakhCrore(sStr);
  if(!isNaN(lakhVal)) return lakhVal;
  // Also handle K suffix if present
  const kMatch=sStr.match(/^([0-9,.]+)\s*[kK]\b/);
  if(kMatch){ const n=parseFloat(kMatch[1].replace(/,/g,'')); if(!isNaN(n)) return n*1e3; }
  const c=cleanNumberString(sStr);
  if(c===""||c==="-") return NaN;
  const n=parseFloat(c);
  return isNaN(n)? NaN : n;
}
function formatIndianPlain(n){
  if(n===""||n==null||isNaN(Number(n))) return "";
  const num=Number(n);
  if(num>=1e7) return (num/1e7).toFixed(2) + " Cr";
  if(num>=1e5) return (num/1e5).toFixed(2) + " L";
  return num.toLocaleString("en-IN",{maximumFractionDigits:2});
}
function formatWithRupeeLakh(n){
  if(n===""||n==null||isNaN(Number(n))) return "₹0.00";
  const num=Number(n);
  if(num>=1e7) return "₹" + (num/1e7).toFixed(2) + " Cr";
  if(num>=1e5) return "₹" + (num/1e5).toFixed(2) + " L";
  return "₹"+num.toLocaleString("en-IN",{minimumFractionDigits:2,maximumFractionDigits:2});
}
// Attach focus/blur: blur shows Lakh/Cr when >=1,00,000, focus shows raw number for editing
function attachIndianInputs(ids){
  ids.forEach(id=>{
    const el=document.getElementById(id); if(!el) return;
    el.addEventListener("focus", ()=>{
      const n=toNumber(el.value);
      if(!isNaN(n) && el.value!=="") el.value=String(n);
      setTimeout(()=>{ try{el.select();}catch(e){} },0);
    });
    el.addEventListener("blur", ()=>{
      const n=toNumber(el.value);
      if(!isNaN(n) && el.value!=="") el.value=formatIndianPlain(n);
    });
    // While typing, allow digits, dot, comma; don't block L/Cr letters entirely but will be parsed on blur
    el.addEventListener("input", ()=>{
      // Allow typing; if user pastes L/Cr, keep it for later parsing — don't strip
    });
  });
}
document.addEventListener("DOMContentLoaded", ()=>{
  attachIndianInputs(["revenueAmount","cogsAmount","opexAmount","fcPrice","beFixed","beRevPer","beVar","simMarketing","simSalaries","simCloud","simOther","fcCustomers","fcGrowth","fcExpGrowth"]);
  // Quick 1L / 1Cr buttons for Revenue Amount
  document.getElementById("revenue1L")?.addEventListener("click", ()=>{
    const el=document.getElementById("revenueAmount"); if(el){ el.value=formatIndianPlain(100000); el.dispatchEvent(new Event("input")); el.focus(); }
  });
  document.getElementById("revenue1Cr")?.addEventListener("click", ()=>{
    const el=document.getElementById("revenueAmount"); if(el){ el.value=formatIndianPlain(10000000); el.dispatchEvent(new Event("input")); el.focus(); }
  });
});
// If DOM already loaded (script at end), attach immediately as fallback
// Also attach 1L/1Cr immediately for script-at-end case
try{
  document.getElementById("revenue1L")?.addEventListener("click", ()=>{
    const el=document.getElementById("revenueAmount"); if(el){ el.value=formatIndianPlain(100000); el.dispatchEvent(new Event("input")); el.focus(); }
  });
  document.getElementById("revenue1Cr")?.addEventListener("click", ()=>{
    const el=document.getElementById("revenueAmount"); if(el){ el.value=formatIndianPlain(10000000); el.dispatchEvent(new Event("input")); el.focus(); }
  });
}catch(e){}
// ===== Display toggle: Full vs Lakh/Cr =====
function updateFmtToggleBtn(){
  const btn=document.getElementById("fmtToggle");
  if(!btn) return;
  btn.textContent= DISPLAY_FMT==="lakh" ? "₹ Lakh" : "₹ Full";
  btn.setAttribute("data-tooltip", DISPLAY_FMT==="lakh" ? "Showing Lakh/Cr (₹1.00 L). Click for full ₹1,00,000" : "Showing full Indian commas. Click for Lakh/Cr");
}
document.addEventListener("DOMContentLoaded", ()=>{
  updateFmtToggleBtn();
  document.getElementById("fmtToggle")?.addEventListener("click", ()=>{
    DISPLAY_FMT = DISPLAY_FMT==="lakh" ? "full" : "lakh";
    localStorage.setItem("display_fmt", DISPLAY_FMT);
    updateFmtToggleBtn();
    renderAll();
  });
});
try{
  updateFmtToggleBtn();
  document.getElementById("fmtToggle")?.addEventListener("click", ()=>{
    DISPLAY_FMT = DISPLAY_FMT==="lakh" ? "full" : "lakh";
    localStorage.setItem("display_fmt", DISPLAY_FMT);
    updateFmtToggleBtn();
    renderAll();
  });
}catch(e){}
try{ attachIndianInputs(["revenueAmount","cogsAmount","opexAmount","fcPrice","beFixed","beRevPer","beVar","simMarketing","simSalaries","simCloud","simOther","fcCustomers","fcGrowth","fcExpGrowth"]); }catch(e){}

// ===== Reusable Tooltip System =====
const TOOLTIP_DEFS = {
  revenue: {title:"Revenue", desc:"Total income generated from sales during the selected period."},
  expenses: {title:"Expenses", desc:"Total business costs recorded during the selected period."},
  cogs: {title:"COGS", desc:"Cost of Goods Sold — direct costs to deliver product/service (hosting, DB, fees)."},
  opex: {title:"Operating Expenses", desc:"Indirect costs: salaries, marketing, software, rent, other."},
  netProfit: {title:"Net Profit", desc:"Revenue minus total expenses (COGS + OPEX). Positive = profit, negative = loss."},
  profitMargin: {title:"Profit Margin", desc:"Percentage of revenue remaining after expenses. (Net Profit / Revenue × 100)"},
  grossProfit: {title:"Gross Profit", desc:"Revenue minus COGS. Shows core product profitability before operating costs."},
  grossMargin: {title:"Gross Margin", desc:"Gross Profit as % of Revenue. Higher = more efficient delivery."},
  burnRate: {title:"Burn Rate", desc:"Average net cash outflow per month when business is loss-making. Burn = |Net Loss|."},
  runway: {title:"Cash Runway", desc:"Estimated months current cash can sustain burn. Runway = Cash Balance / Burn Rate. ∞ if profitable."},
  healthScore: {title:"Financial Health Score", desc:"Overall financial condition 0-100 based on profitability, growth, expense control, cash flow, stability. Calculated transparently from real DB data."},
  revenueGrowth: {title:"Revenue Growth", desc:"Month-over-month change vs previous month. Growth = (Current - Previous)/Previous × 100."},
  expenseGrowth: {title:"Expense Growth", desc:"Month-over-month OPEX change. Rising faster than revenue = warning."},
  variance: {title:"Variance", desc:"Budget vs Actual difference. Variance % = (Actual - Budget)/Budget × 100."},
  breakeven: {title:"Break-Even Point", desc:"Revenue where profit = 0. BE = Fixed Costs / Contribution Margin %. Below BE = loss."},
  contribution: {title:"Contribution Margin", desc:"Revenue per customer minus variable cost. Covers fixed costs."}
};
function metricInfoIcon(key){
  const def = TOOLTIP_DEFS[key];
  if(!def) return "";
  const html = `<div class='tt-title'>${def.title}</div><div>${def.desc}</div>`;
  return `<span class="info-icon" tabindex="0" role="button" aria-label="More info about ${def.title}" data-tooltip-html="${html.replace(/"/g,'&quot;')}">ⓘ</span>`;
}
(function initTooltipSystem(){
  let tip=null, hideTimer=null, pinnedEl=null;
  function ensureTip(){
    if(tip) return tip;
    tip=document.createElement("div");
    tip.className="tooltip-root";
    tip.setAttribute("role","tooltip");
    tip.id="global-tooltip";
    document.body.appendChild(tip);
    return tip;
  }
  function positionTip(trigger){
    const t=ensureTip();
    const rect=trigger.getBoundingClientRect();
    const w=t.offsetWidth, h=t.offsetHeight;
    let top=rect.top - h - 10;
    let left=rect.left + rect.width/2 - w/2;
    let place="top";
    if(top < 8){ top=rect.bottom + 10; place="bottom"; }
    if(left < 8) left=8;
    if(left + w > window.innerWidth - 8) left=window.innerWidth - w - 8;
    t.style.top=top+"px"; t.style.left=left+"px";
    t.classList.toggle("place-top", place==="top");
    t.classList.toggle("place-bottom", place==="bottom");
    const isLight = trigger.closest(".topbar,.card,.content") != null;
    t.classList.toggle("light", isLight);
  }
  function showTip(el){
    const html = el.getAttribute("data-tooltip-html");
    const txt = el.getAttribute("data-tooltip");
    const t=ensureTip();
    if(html) t.innerHTML=html;
    else if(txt) t.innerHTML=`<div>${txt}</div>`;
    else return;
    t.style.display="block";
    requestAnimationFrame(()=>{ positionTip(el); t.classList.add("visible"); });
    el.setAttribute("aria-describedby", t.id);
  }
  function hideTip(el){
    if(!tip) return;
    tip.classList.remove("visible","pinned");
    if(el) el.removeAttribute("aria-describedby");
    clearTimeout(hideTimer);
    hideTimer=setTimeout(()=>{ if(tip && !tip.classList.contains("visible")) tip.style.display="none"; },180);
    pinnedEl=null;
  }
  document.addEventListener("mouseover", e=>{
    const el=e.target.closest("[data-tooltip],[data-tooltip-html]");
    if(el && !el._tipPinned) showTip(el);
  });
  document.addEventListener("mouseout", e=>{
    const el=e.target.closest("[data-tooltip],[data-tooltip-html]");
    if(el && el===pinnedEl) return;
    if(el) hideTip(el);
  });
  document.addEventListener("focusin", e=>{
    const el=e.target.closest("[data-tooltip],[data-tooltip-html]");
    if(el) showTip(el);
  });
  document.addEventListener("focusout", e=>{
    const el=e.target.closest("[data-tooltip],[data-tooltip-html]");
    if(el) hideTip(el);
  });
  document.addEventListener("click", e=>{
    const el=e.target.closest("[data-tooltip],[data-tooltip-html]");
    if(el){
      const isTouch = window.matchMedia("(pointer: coarse)").matches || window.innerWidth<=900;
      if(isTouch){
        e.preventDefault();
        if(pinnedEl===el){ hideTip(el); return; }
        if(pinnedEl) hideTip(pinnedEl);
        showTip(el);
        ensureTip().classList.add("pinned");
        pinnedEl=el; el._tipPinned=true;
        setTimeout(()=>{ el._tipPinned=false; },300);
        return;
      }
    }
    if(pinnedEl && !e.target.closest("#global-tooltip")) hideTip(pinnedEl);
  });
  window.addEventListener("scroll", ()=>{ if(pinnedEl) positionTip(pinnedEl); }, true);
  window.addEventListener("resize", ()=>{ if(pinnedEl) positionTip(pinnedEl); });
})();

function defaultData(){
  const data={business:"AI SaaS Startup", selectedMonth:8,
    months: MONTHS.map((m,i)=>({name:m, year:2026, revenue:[], cogs:[], opex:[], otherIncome:0, otherExpenses:0}))
  };
  data.months[8].revenue=[{id:1, source:"Subscription Revenue", amount:20000}];
  data.months[8].cogs=[{id:1, source:"Cloud Hosting", amount:1000},{id:2, source:"Database", amount:300},{id:3, source:"Payment Fees", amount:200}];
  data.months[8].opex=[{id:1, category:"Marketing", amount:2000},{id:2, category:"Salaries", amount:2000},{id:3, category:"Software", amount:500},{id:4, category:"Other", amount:500}];
   const baseRev=[6000,7000,8000,9000,9500,10000,10500,11000,20000,11500,12000,13000];
  const baseCogs=[900,1050,1200,1350,1425,1500,1575,1650,1500,1725,1800,1950];
  const baseOpex=[4000,4200,4500,4700,4800,5000,5100,5200,5000,5400,5500,5800];
  baseRev.forEach((r,i)=>{
    if(i===8) return;
    data.months[i].revenue=[{id:Date.now()+i, source:"Subscription Revenue", amount:r}];
    data.months[i].cogs=[{id:Date.now()+i+100, source:"Cloud Hosting", amount:Math.round(baseCogs[i]*0.66)},{id:Date.now()+i+200, source:"Database", amount:Math.round(baseCogs[i]*0.2)},{id:Date.now()+i+300, source:"Payment Fees", amount:Math.round(baseCogs[i]*0.14)}];
    data.months[i].opex=[{id:Date.now()+i+400, category:"Marketing", amount:Math.round(baseOpex[i]*0.4)},{id:Date.now()+i+500, category:"Salaries", amount:Math.round(baseOpex[i]*0.4)},{id:Date.now()+i+600, category:"Software", amount:Math.round(baseOpex[i]*0.1)},{id:Date.now()+i+700, category:"Other", amount:Math.round(baseOpex[i]*0.1)}];
  });
  return data;
}
let S = JSON.parse(localStorage.getItem(STORAGE_KEY)||"null") || defaultData();
function save(){ localStorage.setItem(STORAGE_KEY, JSON.stringify(S)); }
function cur(){ return S.months[S.selectedMonth]; }
function pnl(m){
  const rev=m.revenue.reduce((a,b)=>a+b.amount,0);
  const cogs=m.cogs.reduce((a,b)=>a+b.amount,0);
  const opex=m.opex.reduce((a,b)=>a+b.amount,0);
  const gross=rev-cogs;
  const gm= rev? (gross/rev*100):0;
  const op=gross-opex;
  const net=op - m.otherExpenses + m.otherIncome;
  const nm= rev? (net/rev*100):0;
  return {rev,cogs,opex,gross,gm,op,net,nm, status: net>0?"Profit": net<0?"Loss":"Break-even"};
}
function yearly(){
  let rev=0,cogs=0,opex=0;
  S.months.forEach(m=>{rev+=m.revenue.reduce((a,b)=>a+b.amount,0); cogs+=m.cogs.reduce((a,b)=>a+b.amount,0); opex+=m.opex.reduce((a,b)=>a+b.amount,0);});
  const gross=rev-cogs, gm=rev?gross/rev*100:0, op=gross-opex, net=op, nm=rev?net/rev*100:0;
  return {rev,cogs,gross,gm,opex,op,net,nm};
}

// SQL helpers
let sqlMonths=[]; // from /api/months/${CURRENT_BIZ}
let sqlDashboard=null;
let sqlPnlCache=null;
// Mongo helpers (keep SQLite)
let mongoMonths=[];
let mongoDashboard=null;
let mongoPnlCache=null;
async function apiGet(path){
  const r=await fetch(API_BASE+path);
  if(!r.ok) throw new Error(await r.text());
  return r.json();
}
async function apiPost(path, body){
  const r=await fetch(API_BASE+path,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
  if(!r.ok) throw new Error(await r.text());
  return r.json();
}
async function apiDel(path){
  const r=await fetch(API_BASE+path,{method:"DELETE"});
  if(!r.ok) throw new Error(await r.text());
  return r.json();
}
function curMonthId(){ // sql mode
  if(DATA_MODE==="mongo" && mongoMonths.length) return mongoMonths[S.selectedMonth]?.id;
  if(sqlMonths.length) return sqlMonths[S.selectedMonth]?.id;
  return null;
}
async function loadSqlMonths(){
  try{
    sqlMonths=await apiGet(`/api/months/${CURRENT_BIZ}`);
    const status=document.getElementById("dataSourceStatus");
    if(status) status.textContent=`SQL connected — ${sqlMonths.length} months loaded`;
  }catch(e){
    const status=document.getElementById("dataSourceStatus");
    if(status) status.textContent="SQL not reachable — start Flask on :5000";
    console.error(e);
  }
}
async function loadSqlDashboard(){
  try{ sqlDashboard=await apiGet(`/api/dashboard/${CURRENT_BIZ}`); }catch(e){ console.error(e); }
}
async function loadSqlPnl(){
  const mid=curMonthId();
  if(!mid) return;
  try{ sqlPnlCache=await apiGet(`/api/pnl?business_id=${CURRENT_BIZ}&month_id=${mid}`); }catch(e){ console.error(e); }
}
async function loadMongoMonths(){
  try{
    mongoMonths=await apiGet(`/api/mongo/months/${CURRENT_BIZ}`);
    const status=document.getElementById("dataSourceStatus");
    if(status) status.textContent=`Mongo connected — ${mongoMonths.length} months loaded`;
  }catch(e){
    const status=document.getElementById("dataSourceStatus");
    if(status) status.textContent="Mongo not reachable — set MONGO_URI env and start mongod/Atlas. Try Local or SQL.";
    console.error(e);
    throw e;
  }
}
async function loadMongoDashboard(){
  try{ mongoDashboard=await apiGet(`/api/mongo/dashboard/${CURRENT_BIZ}`); }catch(e){ console.error(e); }
}
async function loadMongoPnl(){
  const mid=curMonthId();
  if(!mid) return;
  try{ mongoPnlCache=await apiGet(`/api/mongo/pnl?business_id=${CURRENT_BIZ}&month_id=${mid}`); }catch(e){ console.error(e); }
}

// Navigation
document.querySelectorAll(".nav a").forEach(a=>{
  a.addEventListener("click", e=>{
    document.querySelectorAll(".nav a").forEach(x=>x.classList.remove("active"));
    a.classList.add("active");
    const id=a.dataset.page;
    document.querySelectorAll(".page").forEach(p=>p.classList.remove("active"));
    document.getElementById("page-"+id).classList.add("active");
    if(window.innerWidth<=900) document.querySelector(".sidebar").classList.remove("open");
    renderAll();
  });
});
document.getElementById("mobileToggle")?.addEventListener("click",()=>document.querySelector(".sidebar").classList.toggle("open"));

// Month selector
const monthSel=document.getElementById("monthSelect");
function fillMonthSel(){
  monthSel.innerHTML="";
  let months;
  if(DATA_MODE==="sql" && sqlMonths.length) months=sqlMonths.map(m=>({name:m.month_name, year:m.year}));
  else if(DATA_MODE==="mongo" && mongoMonths.length) months=mongoMonths.map(m=>({name:m.month_name, year:m.year}));
  else months=S.months;
  months.forEach((m,i)=>{
    const o=document.createElement("option"); o.value=i; o.textContent=`${m.name} ${m.year}`; if(i===S.selectedMonth) o.selected=true; monthSel.appendChild(o);
  });
}
monthSel.addEventListener("change", e=>{ S.selectedMonth=parseInt(e.target.value); save(); renderAll(); });
document.getElementById("bizName").textContent=S.business;
document.getElementById("bizNameInput").value=S.business;
document.getElementById("bizNameInput").addEventListener("change", e=>{ S.business=e.target.value; document.getElementById("bizName").textContent=S.business; save(); });

// Data source toggle
const dsSelect=document.getElementById("dataSourceSelect");
if(dsSelect){
  dsSelect.value=DATA_MODE;
  dsSelect.addEventListener("change", async e=>{
    DATA_MODE=e.target.value;
    localStorage.setItem("pnl_mode", DATA_MODE);
    const statusEl=document.getElementById("dataSourceStatus");
    if(DATA_MODE==="sql"){
      statusEl.textContent="Connecting to SQL...";
      await loadSqlMonths();
      await loadSqlDashboard();
      await loadSqlPnl();
      fillMonthSel();
    } else if(DATA_MODE==="mongo"){
      statusEl.textContent="Connecting to MongoDB...";
      try{
        await loadMongoMonths();
        await loadMongoDashboard();
        await loadMongoPnl();
        fillMonthSel();
      }catch(err){
        // stay in mongo but show error; will fallback on render
      }
    } else {
      statusEl.textContent="Using local browser storage";
      sqlDashboard=null; fyCache=null;
    }
    renderAll(); loadFy(); loadAudit();
  });
  // initial status
  const s=document.getElementById("dataSourceStatus");
  if(s) s.textContent= DATA_MODE==="sql" ? "SQL mode — calculations from SQLite via Flask" : DATA_MODE==="mongo" ? "Mongo mode — calculations from MongoDB via Flask" : "Local mode — calculations in browser";
}

document.getElementById("loadDemo").addEventListener("click", async ()=>{
  const btn=document.getElementById("loadDemo");
  const origText=btn.textContent;
  btn.textContent="Loading..."; btn.disabled=true;
  try{
    if(DATA_MODE==="sql"){
      try{
        await apiPost("/api/reset-demo",{business_id: CURRENT_BIZ});
        sqlMonths=[]; sqlDashboard=null; sqlPnlCache=null;
        await loadSqlMonths(); await loadSqlDashboard(); await loadSqlPnl();
        fillMonthSel(); await renderAll();
        alert("✓ Demo data reloaded in SQL DB (AI SaaS Startup - 12 months) via /api/reset-demo");
      }catch(e){
        alert("SQL Load Demo failed: "+e.message+"\nFix: ensure Flask running on :5000 (python pnl-analyzer/backend/app.py)\nFalling back to local reload.");
        localStorage.removeItem(STORAGE_KEY); S=defaultData(); save(); fillMonthSel(); await renderAll();
      }
      return;
    }
    if(DATA_MODE==="mongo"){
      try{
        await apiPost("/api/mongo/reset-demo",{business_id: CURRENT_BIZ});
        mongoMonths=[]; mongoDashboard=null; mongoPnlCache=null;
        await loadMongoMonths(); await loadMongoDashboard(); await loadMongoPnl();
        fillMonthSel(); await renderAll();
        alert("✓ Demo data reloaded in MongoDB (AI SaaS Startup - 12 months) via /api/mongo/reset-demo");
      }catch(e){
        alert("Mongo Load Demo failed: "+e.message+"\nFix: set MONGO_URI env (Atlas or mongodb://localhost:27017) and ensure mongod running. Falling back to local.");
        localStorage.removeItem(STORAGE_KEY); S=defaultData(); save(); fillMonthSel(); await renderAll();
      }
      return;
    }
    localStorage.removeItem(STORAGE_KEY); S=defaultData(); save(); fillMonthSel(); await renderAll(); alert("✓ Demo data loaded (AI SaaS Startup - 12 months) — Local");
  }finally{
    btn.textContent=origText; btn.disabled=false;
  }
});
document.getElementById("resetData").addEventListener("click", async ()=>{
  if(DATA_MODE==="sql"){
    if(confirm("Reset SQL data for current month? This deletes revenue/cogs/expenses for "+ (sqlMonths[S.selectedMonth]?.month_name||"")+"?")){
      const mid=curMonthId();
      const data=sqlPnlCache;
      if(data){
        for(const r of data.revenue) await apiDel(`/api/revenue/${r.id}`);
        for(const c of data.cogs) await apiDel(`/api/cogs/${c.id}`);
        for(const ex of data.expenses) await apiDel(`/api/expenses/${ex.id}`);
        await loadSqlPnl(); await loadSqlDashboard(); renderAll();
      }
    }
    return;
  }
  if(DATA_MODE==="mongo"){
    if(confirm("Mongo: Reset not yet implemented for single month. Use Load Demo to reset all 12 months, or switch to Local/SQL.")){
      // future: call mongo delete
    }
    return;
  }
  if(confirm("Reset all local data?")){ S.months.forEach(m=>{m.revenue=[];m.cogs=[];m.opex=[];}); save(); renderAll();}
});
const syncBtn=document.getElementById("syncToSql");
if(syncBtn){
  syncBtn.addEventListener("click", async ()=>{
    const mid=curMonthId();
    if(!mid){ alert("Select a month first and ensure SQL connected"); return; }
    const m=cur();
    if(!confirm(`Sync local ${m.name} data (${m.revenue.length} revenue, ${m.cogs.length} COGS, ${m.opex.length} expenses) → SQL DB (month_id ${mid})? Existing SQL data for this month will be cleared first to avoid duplicates.`)) return;
    syncBtn.textContent="Syncing..."; syncBtn.disabled=true;
    try{
      // clear existing SQL data for this month to avoid duplicates
      if(sqlPnlCache){
        for(const r of sqlPnlCache.revenue) await apiDel(`/api/revenue/${r.id}`);
        for(const c of sqlPnlCache.cogs) await apiDel(`/api/cogs/${c.id}`);
        for(const ex of sqlPnlCache.expenses) await apiDel(`/api/expenses/${ex.id}`);
      }
      for(const r of m.revenue) await apiPost("/api/revenue",{business_id:CURRENT_BIZ, month_id:mid, source:r.source, amount:r.amount});
      for(const c of m.cogs) await apiPost("/api/cogs",{business_id:CURRENT_BIZ, month_id:mid, source:c.source, amount:c.amount});
      for(const o of m.opex) await apiPost("/api/expenses",{business_id:CURRENT_BIZ, month_id:mid, category:o.category, amount:o.amount});
      await loadSqlPnl(); await loadSqlDashboard();
      renderAll();
      alert(`Synced ${m.name} → SQL successfully! Switch to SQL mode to see it.`);
      document.getElementById("dataSourceStatus").textContent=`Synced ${m.name} to SQL (month_id ${mid})`;
    }catch(e){ alert("Sync failed: "+e.message); console.error(e); }
    finally{ syncBtn.textContent="Sync Local → SQL"; syncBtn.disabled=false; }
  });
}
const syncMongoBtn=document.getElementById("syncToMongo");
if(syncMongoBtn){
  syncMongoBtn.addEventListener("click", async ()=>{
    alert("Mongo Sync: Coming soon — use Load Demo (which seeds Mongo) or manually switch to Mongo mode. Local → Mongo sync will push current month via /api/mongo/import (planned).");
  });
}
// Test SQL connection + snippet runners
const testBtn=document.getElementById("testSqlBtn");
if(testBtn){
  testBtn.addEventListener("click", async ()=>{
    const out=document.getElementById("sqlTestResult");
    out.style.display="block"; out.textContent="Testing...";
    try{
      if(DATA_MODE==="mongo"){
        const h=await apiGet("/api/mongo/health");
        const months=await apiGet(`/api/mongo/months/${CURRENT_BIZ}`);
        const p=await apiGet(`/api/mongo/pnl?business_id=${CURRENT_BIZ}&month_id=${curMonthId()||1}`);
        out.textContent=`✓ Flask OK: ${JSON.stringify(h)}\n✓ Mongo Months: ${months.length} loaded\n✓ Current PNL (${months[S.selectedMonth]?.month_name}): Revenue ${fmt(p.pnl.total_revenue)} | Gross ${fmt(p.pnl.gross_profit)} (${p.pnl.gross_margin}%) | Net ${fmt(p.pnl.net_profit)} (${p.pnl.net_margin}%)\nCalculated in backend/calculations.py (Mongo)`;
        out.style.borderColor="#10b981";
        return;
      }
      const health=await apiGet("/api/health");
      const months=await apiGet(`/api/months/${CURRENT_BIZ}`);
      const pnl=await apiGet(`/api/pnl?business_id=${CURRENT_BIZ}&month_id=${curMonthId()||9}`);
      out.textContent=`✓ Flask OK: ${JSON.stringify(health)}\n✓ Months: ${months.length} loaded\n✓ Current PNL (${months[S.selectedMonth]?.month_name}): Revenue ${fmt(pnl.pnl.total_revenue)} | Gross ${fmt(pnl.pnl.gross_profit)} (${pnl.pnl.gross_margin}%) | Net ${fmt(pnl.pnl.net_profit)} (${pnl.pnl.net_margin}%)\nCalculated in backend/calculations.py`;
      out.style.borderColor="#10b981";
    }catch(e){ 
      const hint = DATA_MODE==="mongo" ? "Mongo not reachable — set MONGO_URI env (e.g., mongodb://localhost:27017 or Atlas) and pip install pymongo" : "SQL error — ensure Flask running: python pnl-analyzer/backend/app.py";
      out.textContent=`✗ Error in ${DATA_MODE} mode: `+e.message+"\n"+hint; out.style.borderColor="#ef4444"; 
    }
  });
}
const runSnippet=document.getElementById("runSqlSnippet");
if(runSnippet){
  runSnippet.addEventListener("click", async ()=>{
    const out=document.getElementById("snippetResult");
    out.style.display="block"; out.textContent="Running fetch with proper monthId...";
    try{
      // FIX: ensure monthId is defined — was `undefined` error before
      const mid=curMonthId()|| sqlMonths[0]?.id || 9;
      if(!mid) throw new Error("monthId undefined — switch to SQL mode first or ensure Flask running");
      const d=await apiGet(`/api/pnl?business_id=${CURRENT_BIZ}&month_id=${mid}`);
      out.innerHTML=`<span style="color:#10b981">✓ Fixed! SQL Result for month_id ${mid} (${sqlMonths.find(m=>m.id===mid)?.month_name||"Sept"}):</span><br>total_revenue: ${fmt(d.pnl.total_revenue)}<br>gross_profit: ${fmt(d.pnl.gross_profit)}<br>net_profit: ${fmt(d.pnl.net_profit)}<br>Source: backend/calculations.py → calculate_pnl() from SQLite<br><span style="color:#94a3b8">Used: fetch(\`http://localhost:5000/api/pnl?business_id=${CURRENT_BIZ}&month_id=\${monthId}\`).then(r=>{if(!r.ok)throw ...} )</span>`;
    }catch(e){ out.innerHTML=`<span style="color:#f87171">✗ Error: ${e.message}</span><br><span style="color:#94a3b8">Fix: Ensure Flask running: python pnl-analyzer/backend/app.py<br>Get valid monthId: fetch("http://localhost:5000/api/months/${CURRENT_BIZ}").then(r=>r.json()).then(m=>console.log(m))</span>`; }
  });
}
const copyBtn=document.getElementById("copySnippet");
if(copyBtn){
  copyBtn.addEventListener("click", ()=>{
    const code=`const monthId = sqlMonths[S.selectedMonth]?.id || 9;
fetch(\`http://localhost:5000/api/pnl?business_id=${CURRENT_BIZ}&month_id=\${monthId}\`)
  .then(r=>{ if(!r.ok) throw new Error(r.statusText); return r.json() })
  .then(d=> console.log(d.pnl.gross_profit)) // from backend/calculations.py
  .catch(err=> console.error("SQL not running on :5000?", err))`;
    navigator.clipboard.writeText(code).then(()=>{ copyBtn.textContent="Copied!"; setTimeout(()=>copyBtn.textContent="Copy code",1500); });
  });
}

// Add forms — uses toNumber() to strip Indian commas, L/Cr, rounding, live validation
function bindAdd(type){
  const btn=document.getElementById("add"+type);
  if(!btn) return;
  const srcEl=document.getElementById(type.toLowerCase()+"Source");
  const amtEl=document.getElementById(type.toLowerCase()+"Amount");
  const err=document.getElementById(type.toLowerCase()+"Error");
  // Live clear: typing clears residual errors (fixes screenshot bug where "Source required" persisted)
  if(srcEl) srcEl.addEventListener("input", ()=>{ if(srcEl.value.trim()) err.textContent=""; });
  if(amtEl) amtEl.addEventListener("input", ()=>{ const v=toNumber(amtEl.value); if(!isNaN(v) && v>=0) err.textContent=""; });
  // Also clear when choosing 1L/1Cr quick buttons
  document.getElementById("revenue1L")?.addEventListener("click", ()=> err.textContent="");
  document.getElementById("revenue1Cr")?.addEventListener("click", ()=> err.textContent="");
  btn.addEventListener("click", async ()=>{
    const src=srcEl.value.trim();
    let amt=toNumber(amtEl.value);
    // Round to 2 decimals for currency, prevent floating errors
    if(!isNaN(amt)) amt=Math.round(amt*100)/100;
    if(!src){ err.textContent="Source required — e.g., Subscription Revenue"; srcEl.focus(); return;}
    if(amt==="" || isNaN(amt)){ err.textContent="Enter valid amount — try 30000, 1.00 L, or 1.00 Cr"; amtEl.focus(); return;}
    if(amt<0){ err.textContent="Amount must be >=0"; amtEl.focus(); return;}
    if(amt>1e12){ err.textContent="Amount too large (max ₹1,00,00,00,00,000)"; return;}
    err.textContent="";
    if(DATA_MODE==="sql"){
      const mid=curMonthId();
      try{
        if(type==="Revenue") await apiPost("/api/revenue",{business_id:CURRENT_BIZ, month_id:mid, source:src, amount:amt});
        if(type==="COGS") await apiPost("/api/cogs",{business_id:CURRENT_BIZ, month_id:mid, source:src, amount:amt});
        if(type==="OPEX") await apiPost("/api/expenses",{business_id:CURRENT_BIZ, month_id:mid, category:src, amount:amt});
        document.getElementById(type.toLowerCase()+"Source").value=""; document.getElementById(type.toLowerCase()+"Amount").value="";
        await loadSqlPnl(); await loadSqlDashboard(); renderAll();
      }catch(e){ err.textContent=e.message; }
      return;
    }
    if(DATA_MODE==="mongo"){
      const mid=curMonthId();
      if(!mid){ err.textContent="Mongo not connected — select valid month"; return; }
      try{
        if(type==="Revenue") await apiPost("/api/mongo/revenue",{business_id:CURRENT_BIZ, month_id:mid, source:src, amount:amt});
        if(type==="COGS") await apiPost("/api/mongo/cogs",{business_id:CURRENT_BIZ, month_id:mid, source:src, amount:amt});
        if(type==="OPEX") await apiPost("/api/mongo/expenses",{business_id:CURRENT_BIZ, month_id:mid, category:src, amount:amt});
        document.getElementById(type.toLowerCase()+"Source").value=""; document.getElementById(type.toLowerCase()+"Amount").value="";
        await loadMongoPnl(); await loadMongoDashboard(); renderAll();
      }catch(e){ err.textContent="Mongo write failed: "+e.message+" — ensure Flask :5000 running"; }
      return;
    }
    const m=cur();
    if(type==="Revenue") m.revenue.push({id:Date.now(), source:src, amount:amt});
    if(type==="COGS") m.cogs.push({id:Date.now(), source:src, amount:amt});
    if(type==="OPEX") m.opex.push({id:Date.now(), category:src, amount:amt});
    document.getElementById(type.toLowerCase()+"Source").value=""; document.getElementById(type.toLowerCase()+"Amount").value="";
    save(); renderAll();
  });
}
bindAdd("Revenue"); bindAdd("COGS"); bindAdd("OPEX");

async function renderLists(){
  const rBody=document.getElementById("revenueList");
  const cBody=document.getElementById("cogsList");
  const oBody=document.getElementById("opexList");
  const spinner=`<tr><td colspan="3" style="text-align:center;padding:20px;color:#64748b"><span style="display:inline-block;width:16px;height:16px;border:2px solid #e2e8f0;border-top-color:#4f46e5;border-radius:999px;animation:spin 0.6s linear infinite;vertical-align:middle;margin-right:8px"></span>Loading...</td></tr>`;
  const emptyRevenue=`<tr><td colspan="3" style="text-align:center;padding:24px;color:#64748b"><div style="font-size:28px">💰</div><div style="margin:8px 0;font-weight:600">No revenue yet</div><div style="font-size:12px;margin-bottom:10px">Add your first source — try <b>Subscription Revenue</b> + <b>1.00 L</b></div><button class="btn btn-ghost" style="padding:6px 10px;font-size:12px" onclick="document.getElementById('revenueSource').value='Subscription Revenue';document.getElementById('revenueAmount').value=formatIndianPlain(100000);document.getElementById('revenueAmount').focus()">+ Use example 1L</button> <button class="btn btn-ghost" style="padding:6px 10px;font-size:12px" onclick="document.getElementById('loadDemo').click()">Load Demo</button></td></tr>`;
  const emptyCogs=`<tr><td colspan="3" style="text-align:center;padding:20px;color:#64748b"><div>📦 No COGS yet</div><div style="font-size:12px;margin-top:6px">Add direct costs like Cloud Hosting ₹10,000</div></td></tr>`;
  const emptyOpex=`<tr><td colspan="3" style="text-align:center;padding:20px;color:#64748b"><div>💸 No expenses yet</div><div style="font-size:12px;margin-top:6px">Add Marketing / Salaries — try ₹20,000</div></td></tr>`;
  if(DATA_MODE==="sql"){
    if(!sqlPnlCache){
      if(rBody) rBody.innerHTML=spinner;
      if(cBody) cBody.innerHTML=spinner;
      if(oBody) oBody.innerHTML=spinner;
      await loadSqlPnl();
    }
    const data=sqlPnlCache;
    if(!data){
      if(rBody) rBody.innerHTML=`<tr><td colspan="3" style="text-align:center;padding:16px;color:#ef4444">Failed to load — Flask :5000 down? <button class="btn btn-ghost" style="padding:4px 8px;margin-left:6px" onclick="loadSqlPnl().then(renderAll)">Retry</button></td></tr>`;
      return;
    }
    if(rBody){
      rBody.innerHTML=data.revenue.map(r=>`<tr><td>${r.source}</td><td>${fmt(r.amount)}</td><td><button class="btn btn-danger" style="padding:4px 8px" onclick="delItem('revenue',${r.id})">Remove</button></td></tr>`).join("")||emptyRevenue.replace("Load Demo","Load Demo (SQL)");
      document.getElementById("totalRevenue").textContent=fmt(data.pnl.total_revenue);
    }
    if(cBody){
      cBody.innerHTML=data.cogs.map(c=>`<tr><td>${c.source}</td><td>${fmt(c.amount)}</td><td><button class="btn btn-danger" style="padding:4px 8px" onclick="delItem('cogs',${c.id})">Remove</button></td></tr>`).join("")||emptyCogs;
      document.getElementById("cogsTotal").textContent=fmt(data.pnl.total_cogs); document.getElementById("grossProfit").textContent=fmt(data.pnl.gross_profit); document.getElementById("grossMargin").textContent=data.pnl.gross_margin.toFixed(2)+"%";
    }
    if(oBody){
      oBody.innerHTML=data.expenses.map(o=>`<tr><td>${o.category}</td><td>${fmt(o.amount)}</td><td><button class="btn btn-danger" style="padding:4px 8px" onclick="delItem('opex',${o.id})">Remove</button></td></tr>`).join("")||emptyOpex;
      document.getElementById("opexTotal").textContent=fmt(data.pnl.total_opex);
    }
    return;
  }
  if(DATA_MODE==="mongo"){
    if(!mongoPnlCache){
      if(rBody) rBody.innerHTML=spinner;
      if(cBody) cBody.innerHTML=spinner;
      if(oBody) oBody.innerHTML=spinner;
      await loadMongoPnl();
    }
    const data=mongoPnlCache;
    if(!data){
      if(rBody) rBody.innerHTML=`<tr><td colspan="3" style="text-align:center;padding:16px;color:#ef4444">Mongo not reachable — check MONGO_URI <button class="btn btn-ghost" style="padding:4px 8px" onclick="loadMongoPnl().then(renderAll)">Retry</button></td></tr>`;
      return;
    }
    if(rBody){
      rBody.innerHTML=data.revenue.map(r=>`<tr><td>${r.source}</td><td>${fmt(r.amount)}</td><td><button class="btn btn-danger" style="padding:4px 8px" onclick="delItem('revenue','${r.id}')">Remove</button></td></tr>`).join("")||`<tr><td colspan="3" style="text-align:center;padding:20px;color:#64748b"><div>💰 No revenue — Mongo empty</div><button class="btn btn-ghost" style="margin-top:8px" onclick="document.getElementById('loadDemo').click()">Load Demo (Mongo)</button></td></tr>`;
      document.getElementById("totalRevenue").textContent=fmt(data.pnl.total_revenue);
    }
    if(cBody){
      cBody.innerHTML=data.cogs.map(c=>`<tr><td>${c.source}</td><td>${fmt(c.amount)}</td><td><button class="btn btn-danger" style="padding:4px 8px" onclick="delItem('cogs','${c.id}')">Remove</button></td></tr>`).join("")||emptyCogs;
      document.getElementById("cogsTotal").textContent=fmt(data.pnl.total_cogs); document.getElementById("grossProfit").textContent=fmt(data.pnl.gross_profit); document.getElementById("grossMargin").textContent=data.pnl.gross_margin.toFixed(2)+"%";
    }
    if(oBody){
      oBody.innerHTML=data.expenses.map(o=>`<tr><td>${o.category}</td><td>${fmt(o.amount)}</td><td><button class="btn btn-danger" style="padding:4px 8px" onclick="delItem('opex','${o.id}')">Remove</button></td></tr>`).join("")||emptyOpex;
      document.getElementById("opexTotal").textContent=fmt(data.pnl.total_opex);
    }
    return;
  }
  const m=cur();
  if(rBody){
    rBody.innerHTML=m.revenue.map(r=>`<tr><td>${r.source}</td><td>${fmt(r.amount)}</td><td><button class="btn btn-danger" style="padding:4px 8px" onclick="delItem('revenue',${r.id})">Remove</button></td></tr>`).join("")||emptyRevenue;
    document.getElementById("totalRevenue").textContent=fmt(m.revenue.reduce((a,b)=>a+b.amount,0));
  }
  if(cBody){
    cBody.innerHTML=m.cogs.map(c=>`<tr><td>${c.source}</td><td>${fmt(c.amount)}</td><td><button class="btn btn-danger" style="padding:4px 8px" onclick="delItem('cogs',${c.id})">Remove</button></td></tr>`).join("")||emptyCogs;
    const p=pnl(m); document.getElementById("cogsTotal").textContent=fmt(p.cogs); document.getElementById("grossProfit").textContent=fmt(p.gross); document.getElementById("grossMargin").textContent=p.gm.toFixed(2)+"%";
  }
  if(oBody){
    oBody.innerHTML=m.opex.map(o=>`<tr><td>${o.category}</td><td>${fmt(o.amount)}</td><td><button class="btn btn-danger" style="padding:4px 8px" onclick="delItem('opex',${o.id})">Remove</button></td></tr>`).join("")||emptyOpex;
    document.getElementById("opexTotal").textContent=fmt(m.opex.reduce((a,b)=>a+b.amount,0));
  }
}
window.delItem=async (type,id)=>{
  if(DATA_MODE==="sql"){
    try{
      if(type==="revenue") await apiDel(`/api/revenue/${id}`);
      if(type==="cogs") await apiDel(`/api/cogs/${id}`);
      if(type==="opex") await apiDel(`/api/expenses/${id}`);
      await loadSqlPnl(); await loadSqlDashboard(); renderAll();
    }catch(e){ alert(e.message); }
    return;
  }
  if(DATA_MODE==="mongo"){
    try{
      if(type==="revenue") await apiDel(`/api/mongo/revenue/${id}`);
      if(type==="cogs") await apiDel(`/api/mongo/cogs/${id}`);
      if(type==="opex") await apiDel(`/api/mongo/expenses/${id}`);
      await loadMongoPnl(); await loadMongoDashboard(); renderAll();
    }catch(e){ alert("Mongo delete failed: "+e.message); }
    return;
  }
  const m=cur();
  if(type==="revenue") m.revenue=m.revenue.filter(x=>x.id!==id && String(x.id)!==String(id));
  if(type==="cogs") m.cogs=m.cogs.filter(x=>x.id!==id && String(x.id)!==String(id));
  if(type==="opex") m.opex=m.opex.filter(x=>x.id!==id && String(x.id)!==String(id));
  save(); renderAll();
};

async function renderDashboard(){
  let p, y, m;
  if(DATA_MODE==="sql"){
    if(!sqlDashboard) await loadSqlDashboard();
    if(!sqlPnlCache) await loadSqlPnl();
    if(!sqlDashboard || !sqlPnlCache) return;
    const idx=S.selectedMonth;
    const monthly=sqlDashboard.monthly[idx];
    p={rev:monthly.total_revenue, cogs:monthly.total_cogs, opex:monthly.total_opex, gross:monthly.gross_profit, gm:monthly.gross_margin, op:monthly.operating_profit, net:monthly.net_profit, nm:monthly.net_margin, status:monthly.status};
    const yr=sqlDashboard.yearly;
    y={rev:yr.annual_revenue, cogs:yr.annual_cogs, gross:yr.annual_gross_profit, gm:yr.annual_gross_margin, opex:yr.annual_opex, op:yr.annual_gross_profit - yr.annual_opex, net:yr.annual_net_profit, nm:yr.annual_net_margin};
    m={name: monthly.month};
  } else if(DATA_MODE==="mongo"){
    if(!mongoDashboard) await loadMongoDashboard();
    if(!mongoPnlCache) await loadMongoPnl();
    if(!mongoDashboard || !mongoPnlCache) return;
    const idx=S.selectedMonth;
    const monthly=mongoDashboard.monthly[idx];
    p={rev:monthly.total_revenue, cogs:monthly.total_cogs, opex:monthly.total_opex, gross:monthly.gross_profit, gm:monthly.gross_margin, op:monthly.operating_profit, net:monthly.net_profit, nm:monthly.net_margin, status:monthly.status};
    const yr=mongoDashboard.yearly;
    y={rev:yr.annual_revenue, cogs:yr.annual_cogs, gross:yr.annual_gross_profit, gm:yr.annual_gross_margin, opex:yr.annual_opex, op:yr.annual_gross_profit - yr.annual_opex, net:yr.annual_net_profit, nm:yr.annual_net_margin};
    m={name: monthly.month};
  } else {
    m=cur(); p=pnl(m); y=yearly();
  }
  const kpis=document.getElementById("kpis");
  if(kpis){
    kpis.innerHTML=`
      <div class="card kpi"><h3>Total Revenue</h3><div class="value">${fmt(p.rev)}</div><div class="sub">${m.name} 2026 ${DATA_MODE==="sql" ? "• SQL" : DATA_MODE==="mongo" ? "• MongoDB" : "• Local"}</div></div>
      <div class="card kpi"><h3>Total COGS</h3><div class="value">${fmt(p.cogs)}</div><div class="sub">${p.rev? (p.cogs/p.rev*100).toFixed(1):0}% of revenue</div></div>
      <div class="card kpi"><h3>Gross Profit</h3><div class="value" style="color:#10b981">${fmt(p.gross)}</div><div class="sub">${p.gm.toFixed(2)}% margin</div></div>
      <div class="card kpi"><h3>Operating Expenses</h3><div class="value">${fmt(p.opex)}</div><div class="sub">Total OPEX</div></div>
      <div class="card kpi ${p.net>=0?'profit':'loss'}"><h3>Net ${p.status}</h3><div class="value" style="color:${p.net>=0?'#10b981':'#ef4444'}">${fmt(p.net)}</div><div class="sub">${p.nm.toFixed(2)}% net margin</div></div>
      <div class="card kpi"><h3>Gross Margin %</h3><div class="value">${p.gm.toFixed(2)}%</div><div class="progress"><div style="width:${Math.min(100,Math.max(0,p.gm))}%"></div></div></div>
      <div class="card kpi"><h3>Net Margin %</h3><div class="value">${p.nm.toFixed(2)}%</div><div class="progress"><div style="width:${Math.min(100,Math.max(0,p.nm))}%; background:${p.nm>=0?'#10b981':'#ef4444'}"></div></div></div>
      <div class="card kpi ${p.net>=0?'profit':'loss'}"><h3>Break-even Status</h3><div class="value">${p.net>=0?'✔ Profitable':'✘ Loss'}</div><div class="sub">${p.net>=0?'Above break-even':'Below break-even'}</div></div>
    `;
  }
  const yEl=document.getElementById("yearlyCards");
  if(yEl){
    yEl.innerHTML=`
      <div class="card"><h3 style="font-size:12px;color:#64748b">Annual Revenue</h3><div style="font-size:20px;font-weight:800">${fmt(y.rev)}</div></div>
      <div class="card"><h3 style="font-size:12px;color:#64748b">Annual COGS</h3><div style="font-size:20px;font-weight:800">${fmt(y.cogs)}</div></div>
      <div class="card"><h3 style="font-size:12px;color:#64748b">Annual Gross Profit</h3><div style="font-size:20px;font-weight:800;color:#10b981">${fmt(y.gross)} · ${y.gm.toFixed(1)}%</div></div>
      <div class="card"><h3 style="font-size:12px;color:#64748b">Annual OPEX</h3><div style="font-size:20px;font-weight:800">${fmt(y.opex)}</div></div>
      <div class="card"><h3 style="font-size:12px;color:#64748b">Annual Net ${y.net>=0?'Profit':'Loss'}</h3><div style="font-size:20px;font-weight:800;color:${y.net>=0?'#10b981':'#ef4444'}">${fmt(y.net)} · ${y.nm.toFixed(1)}%</div></div>
    `;
  }
  const healthEl=document.getElementById("healthGrid");
  if(healthEl){
    let prev;
    if(DATA_MODE==="sql"){
      const idx=S.selectedMonth; const prevIdx=Math.max(0,idx-1);
      const curr=sqlDashboard.monthly[idx]; const prv=sqlDashboard.monthly[prevIdx];
      const growth = prv.total_revenue? ((curr.total_revenue-prv.total_revenue)/prv.total_revenue*100):0;
      const expenseGrowth = prv.total_opex? ((curr.total_opex-prv.total_opex)/prv.total_opex*100):0;
      const burn = curr.net_profit<0? Math.abs(curr.net_profit):0;
      const runway = burn? (y.net>0? "∞ (profitable)": "N/A - estimate cash / burn"): "∞";
      healthEl.innerHTML=`
        <div class="health-item"><div class="label">Revenue Growth (MoM)</div><div class="val" style="color:${growth>=0?'#10b981':'#ef4444'}">${growth.toFixed(1)}%</div><div class="sub" style="font-size:12px;color:#64748b">vs ${prv.month} • SQL</div></div>
        <div class="health-item"><div class="label">Gross Margin</div><div class="val">${curr.gross_margin.toFixed(1)}%</div><div class="sub" style="font-size:12px;color:#64748b">${curr.gross_margin>60?'Excellent':curr.gross_margin>40?'Healthy':'Low'}</div></div>
        <div class="health-item"><div class="label">Net Margin</div><div class="val" style="color:${curr.net_margin>=0?'#10b981':'#ef4444'}">${curr.net_margin.toFixed(1)}%</div><div class="sub" style="font-size:12px;color:#64748b">${curr.net_margin>20?'Strong':curr.net_margin>0?'Positive':'Negative'}</div></div>
        <div class="health-item"><div class="label">Expense Growth</div><div class="val">${expenseGrowth.toFixed(1)}%</div><div class="sub" style="font-size:12px;color:#64748b">OPEX MoM</div></div>
        <div class="health-item"><div class="label">Burn Rate</div><div class="val">${burn? fmt(burn)+'/mo':'₹0 (profitable)'}</div><div class="sub" style="font-size:12px;color:#64748b">Monthly net loss • from SQLite</div></div>
        <div class="health-item"><div class="label">Runway</div><div class="val">${runway}</div><div class="sub" style="font-size:12px;color:#64748b">Estimates based on SQL data</div></div>
      `;
      return;
    }
    if(DATA_MODE==="mongo"){
      const idx=S.selectedMonth; const prevIdx=Math.max(0,idx-1);
      const curr=mongoDashboard.monthly[idx]; const prv=mongoDashboard.monthly[prevIdx];
      const growth = prv.total_revenue? ((curr.total_revenue-prv.total_revenue)/prv.total_revenue*100):0;
      const expenseGrowth = prv.total_opex? ((curr.total_opex-prv.total_opex)/prv.total_opex*100):0;
      const burn = curr.net_profit<0? Math.abs(curr.net_profit):0;
      const runway = burn? (y.net>0? "∞ (profitable)": "N/A - estimate cash / burn"): "∞";
      healthEl.innerHTML=`
        <div class="health-item"><div class="label">Revenue Growth (MoM)</div><div class="val" style="color:${growth>=0?'#10b981':'#ef4444'}">${growth.toFixed(1)}%</div><div class="sub" style="font-size:12px;color:#64748b">vs ${prv.month} • MongoDB</div></div>
        <div class="health-item"><div class="label">Gross Margin</div><div class="val">${curr.gross_margin.toFixed(1)}%</div><div class="sub" style="font-size:12px;color:#64748b">${curr.gross_margin>60?'Excellent':curr.gross_margin>40?'Healthy':'Low'}</div></div>
        <div class="health-item"><div class="label">Net Margin</div><div class="val" style="color:${curr.net_margin>=0?'#10b981':'#ef4444'}">${curr.net_margin.toFixed(1)}%</div><div class="sub" style="font-size:12px;color:#64748b">${curr.net_margin>20?'Strong':curr.net_margin>0?'Positive':'Negative'}</div></div>
        <div class="health-item"><div class="label">Expense Growth</div><div class="val">${expenseGrowth.toFixed(1)}%</div><div class="sub" style="font-size:12px;color:#64748b">OPEX MoM</div></div>
        <div class="health-item"><div class="label">Burn Rate</div><div class="val">${burn? fmt(burn)+'/mo':'₹0 (profitable)'}</div><div class="sub" style="font-size:12px;color:#64748b">Monthly net loss • from MongoDB</div></div>
        <div class="health-item"><div class="label">Runway</div><div class="val">${runway}</div><div class="sub" style="font-size:12px;color:#64748b">Estimates based on MongoDB data</div></div>
      `;
      return;
    }
    const prevIdx=Math.max(0,S.selectedMonth-1);
    prev=pnl(S.months[prevIdx]);
    const growth = prev.rev? ((p.rev-prev.rev)/prev.rev*100):0;
    const expenseGrowth = prev.opex? ((p.opex-prev.opex)/prev.opex*100):0;
    const burn = p.net<0? Math.abs(p.net):0;
    const runway = burn? (y.net>0? "∞ (profitable)": "N/A - estimate cash / burn"): "∞";
    healthEl.innerHTML=`
      <div class="health-item"><div class="label">Revenue Growth (MoM)</div><div class="val" style="color:${growth>=0?'#10b981':'#ef4444'}">${growth.toFixed(1)}%</div><div class="sub" style="font-size:12px;color:#64748b">vs ${S.months[prevIdx].name}</div></div>
      <div class="health-item"><div class="label">Gross Margin</div><div class="val">${p.gm.toFixed(1)}%</div><div class="sub" style="font-size:12px;color:#64748b">${p.gm>60?'Excellent':p.gm>40?'Healthy':'Low'}</div></div>
      <div class="health-item"><div class="label">Net Margin</div><div class="val" style="color:${p.nm>=0?'#10b981':'#ef4444'}">${p.nm.toFixed(1)}%</div><div class="sub" style="font-size:12px;color:#64748b">${p.nm>20?'Strong':p.nm>0?'Positive':'Negative'}</div></div>
      <div class="health-item"><div class="label">Expense Growth</div><div class="val">${expenseGrowth.toFixed(1)}%</div><div class="sub" style="font-size:12px;color:#64748b">OPEX MoM</div></div>
      <div class="health-item"><div class="label">Burn Rate</div><div class="val">${burn? fmt(burn)+'/mo':'₹0 (profitable)'}</div><div class="sub" style="font-size:12px;color:#64748b">Monthly net loss</div></div>
      <div class="health-item"><div class="label">Runway</div><div class="val">${runway}</div><div class="sub" style="font-size:12px;color:#64748b">Estimates based on entered data</div></div>
    `;
  }
}

async function renderPnlTable(){
  const el=document.getElementById("pnlTable");
  if(!el) return;
  let m, p, revRows, cogsRows, opexRows;
  if(DATA_MODE==="sql"){
    if(!sqlPnlCache) await loadSqlPnl();
    const d=sqlPnlCache;
    if(!d) return;
    p={rev:d.pnl.total_revenue, cogs:d.pnl.total_cogs, gross:d.pnl.gross_profit, gm:d.pnl.gross_margin, opex:d.pnl.total_opex, op:d.pnl.operating_profit, net:d.pnl.net_profit, nm:d.pnl.net_margin, status:d.pnl.status};
    revRows=d.revenue.map(r=>`<tr><td>${r.source}</td><td style="text-align:right">${fmt(r.amount)}</td></tr>`).join("")||`<tr><td style="color:#94a3b8">No revenue</td><td style="text-align:right">₹0.00</td></tr>`;
    cogsRows=d.cogs.map(c=>`<tr><td>${c.source}</td><td style="text-align:right">${fmt(c.amount)}</td></tr>`).join("")||`<tr><td style="color:#94a3b8">No COGS</td><td style="text-align:right">₹0.00</td></tr>`;
    opexRows=d.expenses.map(o=>`<tr><td>${o.category}</td><td style="text-align:right">${fmt(o.amount)}</td></tr>`).join("")||`<tr><td style="color:#94a3b8">No expenses</td><td style="text-align:right">₹0.00</td></tr>`;
    el.innerHTML=`
      <table class="table">
        <tr style="background:#f1f5f9"><th colspan="2">REVENUE • SQL</th></tr>
        ${revRows}
        <tr class="pl-total"><td>TOTAL REVENUE</td><td style="text-align:right">${fmt(p.rev)}</td></tr>
        <tr style="background:#f1f5f9"><th colspan="2">COGS • SQL</th></tr>
        ${cogsRows}
        <tr class="pl-total"><td>TOTAL COGS</td><td style="text-align:right">${fmt(p.cogs)}</td></tr>
        <tr style="background:#ecfdf5"><td><strong>GROSS PROFIT</strong></td><td style="text-align:right"><strong>${fmt(p.gross)}</strong></td></tr>
        <tr style="background:#ecfdf5"><td>GROSS MARGIN</td><td style="text-align:right">${p.gm.toFixed(2)}%</td></tr>
        <tr style="background:#f1f5f9"><th colspan="2">OPERATING EXPENSES • SQL</th></tr>
        ${opexRows}
        <tr class="pl-total"><td>TOTAL OPEX</td><td style="text-align:right">${fmt(p.opex)}</td></tr>
        <tr style="background:${p.op>=0?'#ecfdf5':'#fef2f2'}"><td><strong>OPERATING PROFIT</strong></td><td style="text-align:right"><strong>${fmt(p.op)}</strong></td></tr>
        <tr style="background:${p.net>=0?'#ecfdf5':'#fef2f2'}"><td><strong>NET ${p.status.toUpperCase()}</strong></td><td style="text-align:right"><strong>${fmt(p.net)}</strong></td></tr>
        <tr style="background:${p.net>=0?'#ecfdf5':'#fef2f2'}"><td>NET MARGIN</td><td style="text-align:right">${p.nm.toFixed(2)}%</td></tr>
      </table>
      <p style="font-size:12px;color:#64748b;margin-top:8px">* Calculated in backend/calculations.py from SQLite • Not financial advice.</p>
    `;
    return;
  }
  if(DATA_MODE==="mongo"){
    if(!mongoPnlCache) await loadMongoPnl();
    const d=mongoPnlCache;
    if(!d) return;
    p={rev:d.pnl.total_revenue, cogs:d.pnl.total_cogs, gross:d.pnl.gross_profit, gm:d.pnl.gross_margin, opex:d.pnl.total_opex, op:d.pnl.operating_profit, net:d.pnl.net_profit, nm:d.pnl.net_margin, status:d.pnl.status};
    revRows=d.revenue.map(r=>`<tr><td>${r.source}</td><td style="text-align:right">${fmt(r.amount)}</td></tr>`).join("")||`<tr><td style="color:#94a3b8">No revenue — Mongo</td><td style="text-align:right">₹0.00</td></tr>`;
    cogsRows=d.cogs.map(c=>`<tr><td>${c.source}</td><td style="text-align:right">${fmt(c.amount)}</td></tr>`).join("")||`<tr><td style="color:#94a3b8">No COGS — Mongo</td><td style="text-align:right">₹0.00</td></tr>`;
    opexRows=d.expenses.map(o=>`<tr><td>${o.category}</td><td style="text-align:right">${fmt(o.amount)}</td></tr>`).join("")||`<tr><td style="color:#94a3b8">No expenses — Mongo</td><td style="text-align:right">₹0.00</td></tr>`;
    el.innerHTML=`
      <table class="table">
        <tr style="background:#f1f5f9"><th colspan="2">REVENUE • MongoDB</th></tr>
        ${revRows}
        <tr class="pl-total"><td>TOTAL REVENUE</td><td style="text-align:right">${fmt(p.rev)}</td></tr>
        <tr style="background:#f1f5f9"><th colspan="2">COGS • MongoDB</th></tr>
        ${cogsRows}
        <tr class="pl-total"><td>TOTAL COGS</td><td style="text-align:right">${fmt(p.cogs)}</td></tr>
        <tr style="background:#ecfdf5"><td><strong>GROSS PROFIT</strong></td><td style="text-align:right"><strong>${fmt(p.gross)}</strong></td></tr>
        <tr style="background:#ecfdf5"><td>GROSS MARGIN</td><td style="text-align:right">${p.gm.toFixed(2)}%</td></tr>
        <tr style="background:#f1f5f9"><th colspan="2">OPERATING EXPENSES • MongoDB</th></tr>
        ${opexRows}
        <tr class="pl-total"><td>TOTAL OPEX</td><td style="text-align:right">${fmt(p.opex)}</td></tr>
        <tr style="background:${p.op>=0?'#ecfdf5':'#fef2f2'}"><td><strong>OPERATING PROFIT</strong></td><td style="text-align:right"><strong>${fmt(p.op)}</strong></td></tr>
        <tr style="background:${p.net>=0?'#ecfdf5':'#fef2f2'}"><td><strong>NET ${p.status.toUpperCase()}</strong></td><td style="text-align:right"><strong>${fmt(p.net)}</strong></td></tr>
        <tr style="background:${p.net>=0?'#ecfdf5':'#fef2f2'}"><td>NET MARGIN</td><td style="text-align:right">${p.nm.toFixed(2)}%</td></tr>
      </table>
      <p style="font-size:12px;color:#64748b;margin-top:8px">* Calculated in backend/calculations.py from MongoDB • Not financial advice.</p>
    `;
    return;
  }
  m=cur(); p=pnl(m);
  revRows=m.revenue.map(r=>`<tr><td>${r.source}</td><td style="text-align:right">${fmt(r.amount)}</td></tr>`).join("")||`<tr><td style="color:#94a3b8">No revenue</td><td style="text-align:right">₹0.00</td></tr>`;
  cogsRows=m.cogs.map(c=>`<tr><td>${c.source}</td><td style="text-align:right">${fmt(c.amount)}</td></tr>`).join("")||`<tr><td style="color:#94a3b8">No COGS</td><td style="text-align:right">₹0.00</td></tr>`;
  opexRows=m.opex.map(o=>`<tr><td>${o.category}</td><td style="text-align:right">${fmt(o.amount)}</td></tr>`).join("")||`<tr><td style="color:#94a3b8">No expenses</td><td style="text-align:right">₹0.00</td></tr>`;
  el.innerHTML=`
    <table class="table">
      <tr style="background:#f1f5f9"><th colspan="2">REVENUE</th></tr>
      ${revRows}
      <tr class="pl-total"><td>TOTAL REVENUE</td><td style="text-align:right">${fmt(p.rev)}</td></tr>
      <tr style="background:#f1f5f9"><th colspan="2">COGS</th></tr>
      ${cogsRows}
      <tr class="pl-total"><td>TOTAL COGS</td><td style="text-align:right">${fmt(p.cogs)}</td></tr>
      <tr style="background:#ecfdf5"><td><strong>GROSS PROFIT</strong></td><td style="text-align:right"><strong>${fmt(p.gross)}</strong></td></tr>
      <tr style="background:#ecfdf5"><td>GROSS MARGIN</td><td style="text-align:right">${p.gm.toFixed(2)}%</td></tr>
      <tr style="background:#f1f5f9"><th colspan="2">OPERATING EXPENSES</th></tr>
      ${opexRows}
      <tr class="pl-total"><td>TOTAL OPEX</td><td style="text-align:right">${fmt(p.opex)}</td></tr>
      <tr style="background:${p.op>=0?'#ecfdf5':'#fef2f2'}"><td><strong>OPERATING PROFIT</strong></td><td style="text-align:right"><strong>${fmt(p.op)}</strong></td></tr>
      <tr style="background:${p.net>=0?'#ecfdf5':'#fef2f2'}"><td><strong>NET ${p.status.toUpperCase()}</strong></td><td style="text-align:right"><strong>${fmt(p.net)}</strong></td></tr>
      <tr style="background:${p.net>=0?'#ecfdf5':'#fef2f2'}"><td>NET MARGIN</td><td style="text-align:right">${p.nm.toFixed(2)}%</td></tr>
    </table>
    <p style="font-size:12px;color:#64748b;margin-top:8px">* Estimates based on user-entered data. Not financial advice.</p>
  `;
}

// Charts
let charts={};
async function renderCharts(){
  let labels, revs, cogss, opexes, profits, gms, nms;
  if(DATA_MODE==="sql"){
    if(!sqlDashboard) await loadSqlDashboard();
    if(!sqlDashboard) return;
    labels=sqlDashboard.monthly.map(m=>m.month.slice(0,3));
    revs=sqlDashboard.monthly.map(m=>m.total_revenue);
    cogss=sqlDashboard.monthly.map(m=>m.total_cogs);
    opexes=sqlDashboard.monthly.map(m=>m.total_opex);
    profits=sqlDashboard.monthly.map(m=>m.net_profit);
    gms=sqlDashboard.monthly.map(m=>m.gross_margin);
    nms=sqlDashboard.monthly.map(m=>m.net_margin);
  } else if(DATA_MODE==="mongo"){
    if(!mongoDashboard) await loadMongoDashboard();
    if(!mongoDashboard) return;
    labels=mongoDashboard.monthly.map(m=>m.month.slice(0,3));
    revs=mongoDashboard.monthly.map(m=>m.total_revenue);
    cogss=mongoDashboard.monthly.map(m=>m.total_cogs);
    opexes=mongoDashboard.monthly.map(m=>m.total_opex);
    profits=mongoDashboard.monthly.map(m=>m.net_profit);
    gms=mongoDashboard.monthly.map(m=>m.gross_margin);
    nms=mongoDashboard.monthly.map(m=>m.net_margin);
  } else {
    labels=S.months.map(m=>m.name.slice(0,3));
    revs=S.months.map(m=>m.revenue.reduce((a,b)=>a+b.amount,0));
    cogss=S.months.map(m=>m.cogs.reduce((a,b)=>a+b.amount,0));
    opexes=S.months.map(m=>m.opex.reduce((a,b)=>a+b.amount,0));
    profits=S.months.map(m=>pnl(m).net);
    gms=S.months.map(m=>pnl(m).gm);
    nms=S.months.map(m=>pnl(m).nm);
  }
  Object.values(charts).forEach(c=>{ try{c.destroy();}catch(e){}});
  charts={};
  const ctx1=document.getElementById("chartRevExp");
  if(ctx1){
    charts.a=new Chart(ctx1,{type:'bar',data:{labels, datasets:[
      {label:'Revenue', data:revs, backgroundColor:'#4f46e5'},
      {label:'COGS', data:cogss, backgroundColor:'#f59e0b'},
      {label:'OPEX', data:opexes, backgroundColor:'#ef4444'},
      {label:'Net Profit', data:profits, type:'line', borderColor:'#10b981', backgroundColor:'#10b981', tension:.3}
    ]}, options:{responsive:true, maintainAspectRatio:false, plugins:{legend:{position:'bottom'}}}} );
  }
  const ctx2=document.getElementById("chartProfitTrend");
  if(ctx2){
    charts.b=new Chart(ctx2,{type:'line',data:{labels, datasets:[{label:'Net Profit', data:profits, borderColor:'#4f46e5', backgroundColor:'rgba(79,70,229,.1)', fill:true, tension:.4}]}, options:{responsive:true, maintainAspectRatio:false}});
  }
  const ctx3=document.getElementById("chartExpenseDonut");
  if(ctx3){
    let catMap={};
    if(DATA_MODE==="sql" && sqlPnlCache){
      sqlPnlCache.expenses.forEach(o=>catMap[o.category]=(catMap[o.category]||0)+o.amount);
      sqlPnlCache.cogs.forEach(c=>catMap[c.source]=(catMap[c.source]||0)+c.amount);
    } else if(DATA_MODE==="mongo" && mongoPnlCache){
      mongoPnlCache.expenses.forEach(o=>catMap[o.category]=(catMap[o.category]||0)+o.amount);
      mongoPnlCache.cogs.forEach(c=>catMap[c.source]=(catMap[c.source]||0)+c.amount);
    } else {
      cur().opex.forEach(o=>catMap[o.category]=(catMap[o.category]||0)+o.amount);
      cur().cogs.forEach(c=>catMap[c.source]=(catMap[c.source]||0)+c.amount);
    }
    const labelsD=Object.keys(catMap); const dataD=Object.values(catMap);
    if(labelsD.length){
      charts.c=new Chart(ctx3,{type:'doughnut',data:{labels:labelsD, datasets:[{data:dataD, backgroundColor:['#4f46e5','#06b6d4','#f59e0b','#10b981','#ef4444','#7c3aed','#eab308']}]}, options:{responsive:true, maintainAspectRatio:false, plugins:{legend:{position:'bottom'}}}});
    }
  }
  const ctx4=document.getElementById("chartMargins");
  if(ctx4){
    charts.d=new Chart(ctx4,{type:'line',data:{labels, datasets:[
      {label:'Gross Margin %', data:gms, borderColor:'#10b981', tension:.3},
      {label:'Net Margin %', data:nms, borderColor:'#4f46e5', tension:.3}
    ]}, options:{responsive:true, maintainAspectRatio:false}});
  }
  const ctxF=document.getElementById("chartForecast");
  if(ctxF && window.forecastData){
    charts.f=new Chart(ctxF,{type:'line',data:{labels: window.forecastData.map(r=>"M"+r.month), datasets:[
      {label:'Revenue', data: window.forecastData.map(r=>r.revenue), borderColor:'#4f46e5'},
      {label:'Profit', data: window.forecastData.map(r=>r.profit), borderColor:'#10b981'}
    ]}, options:{responsive:true, maintainAspectRatio:false}});
  }
}

// Break-even — uses toNumber() to handle Indian commas
async function renderBreakEven(){
  const fixed=toNumber(document.getElementById("beFixed")?.value)||5000;
  const revPer=toNumber(document.getElementById("beRevPer")?.value)||10;
  const varCost=toNumber(document.getElementById("beVar")?.value)||2;
  const contrib=revPer-varCost;
  const el=document.getElementById("beResult");
  if(!el) return;
  if(contrib<=0){ el.innerHTML=`<div style="color:#ef4444">Contribution margin must be >0 (Revenue per customer > Variable cost)</div>`; return;}
  const beCust=(fixed/contrib);
  const beRev=beCust*revPer;
  let curRev=0;
  if(DATA_MODE==="sql"){
    if(sqlPnlCache) curRev=sqlPnlCache.pnl.total_revenue;
    else { const mid=curMonthId(); if(mid){ try{ const d=await apiGet(`/api/pnl?business_id=${CURRENT_BIZ}&month_id=${mid}`); curRev=d.pnl.total_revenue;}catch(e){} } }
  } else {
    curRev=cur().revenue.reduce((a,b)=>a+b.amount,0);
  }
  el.innerHTML=`
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:12px 0">
      <div class="card"><div style="font-size:12px;color:#64748b">Contribution Margin</div><div style="font-size:20px;font-weight:800">${fmt(contrib)} / customer</div></div>
      <div class="card" style="border:2px solid #4f46e5"><div style="font-size:12px;color:#64748b">Break-even Customers</div><div style="font-size:20px;font-weight:800">${Math.ceil(beCust).toLocaleString()} customers</div></div>
      <div class="card"><div style="font-size:12px;color:#64748b">Break-even Revenue</div><div style="font-size:20px;font-weight:800">${fmt(beRev)}</div></div>
    </div>
    <div style="background:#f8fafc;padding:12px;border-radius:12px;border:1px solid #e2e8f0">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><div style="flex:1;height:12px;background:#e2e8f0;border-radius:999px;overflow:hidden"><div style="width:${Math.min(100, (curRev/beRev*100))}%;height:100%;background:#10b981"></div></div><span style="font-size:12px">${(curRev/beRev*100).toFixed(1)}% of break-even</span></div>
      <div style="font-size:12px;color:#64748b">Formula: Fixed Costs ÷ (Revenue per Customer − Variable Cost) = ${fixed} ÷ ${contrib.toFixed(2)} = ${beCust.toFixed(2)} customers. Current month revenue ${fmt(curRev)} vs break-even ${fmt(beRev)} ${DATA_MODE==="sql"?"• from SQL":""}</div>
    </div>
  `;
}
["beFixed","beRevPer","beVar"].forEach(id=>document.getElementById(id)?.addEventListener("input", renderBreakEven));

// Simulator — uses toNumber() for monetary inputs
function renderSimulator(){
  const cust=parseInt(cleanNumberString(document.getElementById("simCustomers")?.value)||1000);
  const price=toNumber(document.getElementById("simPrice")?.value)||10;
  const marketing=toNumber(document.getElementById("simMarketing")?.value)||2000;
  const salaries=toNumber(document.getElementById("simSalaries")?.value)||2000;
  const cloud=toNumber(document.getElementById("simCloud")?.value)||1500;
  const other=toNumber(document.getElementById("simOther")?.value)||1000;
  const rev=cust*price;
  const cogs=cloud;
  const gross=rev-cogs;
  const opex=marketing+salaries+other;
  const net=gross-opex;
  const gm=rev?gross/rev*100:0; const nm=rev?net/rev*100:0;
  const el=document.getElementById("simResult");
  if(!el) return;
  el.innerHTML=`
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px">
      <div class="card"><div style="font-size:12px;color:#64748b">Revenue</div><div style="font-size:18px;font-weight:800">${fmt(rev)}</div><div style="font-size:12px;color:#64748b">${cust.toLocaleString()} × ${fmt(price)}</div></div>
      <div class="card"><div style="font-size:12px;color:#64748b">Gross Profit</div><div style="font-size:18px;font-weight:800;color:#10b981">${fmt(gross)} · ${gm.toFixed(1)}%</div></div>
      <div class="card" style="border:2px solid ${net>=0?'#10b981':'#ef4444'}"><div style="font-size:12px;color:#64748b">Net ${net>=0?'Profit':'Loss'}</div><div style="font-size:18px;font-weight:800;color:${net>=0?'#10b981':'#ef4444'}">${fmt(net)} · ${nm.toFixed(1)}%</div></div>
    </div>
    <div style="margin-top:12px;display:flex;gap:8px">
      <button class="btn btn-ghost" onclick="applyScenario('conservative')">Conservative (0.8x)</button>
      <button class="btn btn-ghost" onclick="applyScenario('expected')">Expected (1x)</button>
      <button class="btn btn-ghost" onclick="applyScenario('aggressive')">Aggressive (1.5x)</button>
    </div>
  `;
  document.getElementById("simCustomersVal").textContent=cust.toLocaleString();
  document.getElementById("simPriceVal").textContent=fmt(price);
}
["simCustomers","simPrice","simMarketing","simSalaries","simCloud","simOther"].forEach(id=>document.getElementById(id)?.addEventListener("input", renderSimulator));
window.applyScenario=(type)=>{
  const map={conservative:0.8, expected:1, aggressive:1.5};
  const m=map[type]; document.getElementById("simCustomers").value=Math.round(1000*m); renderSimulator();
};

// Forecast - uses backend when SQL mode — uses toNumber() for commas
async function renderForecast(){
  const sc=parseInt(cleanNumberString(document.getElementById("fcCustomers")?.value)||1000);
  const gr=toNumber(document.getElementById("fcGrowth")?.value)||10;
  const price=toNumber(document.getElementById("fcPrice")?.value)||10;
  const eg=toNumber(document.getElementById("fcExpGrowth")?.value)||4;
  let opexBase, cogsPct;
  if(DATA_MODE==="sql" && sqlPnlCache){
    opexBase=sqlPnlCache.pnl.total_opex || 5000;
    cogsPct= sqlPnlCache.pnl.total_revenue ? (sqlPnlCache.pnl.total_cogs / sqlPnlCache.pnl.total_revenue*100) : 15;
  } else {
    opexBase=cur().opex.reduce((a,b)=>a+b.amount,0)||5000;
    cogsPct= cur().revenue.reduce((a,b)=>a+b.amount,0) ? (cur().cogs.reduce((a,b)=>a+b.amount,0)/cur().revenue.reduce((a,b)=>a+b.amount,0)*100):15;
  }
  let rows;
  if(DATA_MODE==="sql"){
    try{
      rows=await apiGet(`/api/forecast?start_customers=${sc}&growth=${gr}&price=${price}&cogs_pct=${cogsPct}&opex_base=${opexBase}&opex_growth=${eg}`);
    }catch(e){ console.error(e); rows=[]; }
  } else {
    rows=[];
    let customers=sc; let opex=opexBase;
    for(let m=1;m<=12;m++){
      if(m>1){ customers=Math.round(customers*(1+gr/100)); opex= +(opex*(1+eg/100)).toFixed(2); }
      const rev=customers*price; const cogs=rev*cogsPct/100; const gross=rev-cogs; const profit=gross-opex;
      rows.push({month:m, customers, revenue:rev, cogs, opex, profit, gm: rev?gross/rev*100:0, nm: rev?profit/rev*100:0});
    }
  }
  window.forecastData=rows;
  const tbody=document.getElementById("forecastBody");
  if(tbody){
    tbody.innerHTML=rows.map(r=>`<tr><td>Month ${r.month}</td><td>${r.customers.toLocaleString()}</td><td>${fmt(r.revenue)}</td><td>${fmt(r.cogs)}</td><td>${fmt(r.opex)}</td><td style="color:${r.profit>=0?'#10b981':'#ef4444'};font-weight:700">${fmt(r.profit)}</td></tr>`).join("");
  }
  renderCharts();
}
["fcCustomers","fcGrowth","fcPrice","fcExpGrowth"].forEach(id=>document.getElementById(id)?.addEventListener("input", renderForecast));

// Export - switch by mode
document.getElementById("exportCsv")?.addEventListener("click", async ()=>{
  if(DATA_MODE==="sql"){
    if(!sqlPnlCache) await loadSqlPnl();
    const d=sqlPnlCache; let csv=`P&L Statement - ${sqlMonths[S.selectedMonth]?.month_name} 2026 (SQL)\n`;
    csv+="Revenue\n"; d.revenue.forEach(r=>csv+=`${r.source},${r.amount}\n`); csv+=`TOTAL REVENUE,${d.pnl.total_revenue}\n`;
    csv+="COGS\n"; d.cogs.forEach(c=>csv+=`${c.source},${c.amount}\n`); csv+=`TOTAL COGS,${d.pnl.total_cogs}\n`;
    csv+=`GROSS PROFIT,${d.pnl.gross_profit}\nGROSS MARGIN,${d.pnl.gross_margin}%\n`;
    csv+="OPEX\n"; d.expenses.forEach(o=>csv+=`${o.category},${o.amount}\n`); csv+=`TOTAL OPEX,${d.pnl.total_opex}\n`;
    csv+=`OPERATING PROFIT,${d.pnl.operating_profit}\nNET PROFIT,${d.pnl.net_profit}\nNET MARGIN,${d.pnl.net_margin}%\n`;
    const blob=new Blob([csv],{type:"text/csv"}); const url=URL.createObjectURL(blob); const a=document.createElement("a"); a.href=url; a.download=`P&L_SQL_${sqlMonths[S.selectedMonth]?.month_name}_2026.csv`; a.click(); URL.revokeObjectURL(url); return;
  }
  const m=cur(); const p=pnl(m);
  let csv="P&L Statement - "+m.name+" 2026\n";
  csv+="Revenue\n"; m.revenue.forEach(r=>csv+=`${r.source},${r.amount}\n`); csv+=`TOTAL REVENUE,${p.rev}\n`;
  csv+="COGS\n"; m.cogs.forEach(c=>csv+=`${c.source},${c.amount}\n`); csv+=`TOTAL COGS,${p.cogs}\n`;
  csv+=`GROSS PROFIT,${p.gross}\nGROSS MARGIN,${p.gm}%\n`;
  csv+="OPEX\n"; m.opex.forEach(o=>csv+=`${o.category},${o.amount}\n`); csv+=`TOTAL OPEX,${p.opex}\n`;
  csv+=`OPERATING PROFIT,${p.op}\nNET PROFIT,${p.net}\nNET MARGIN,${p.nm}%\n`;
  const blob=new Blob([csv],{type:"text/csv"}); const url=URL.createObjectURL(blob); const a=document.createElement("a"); a.href=url; a.download=`P&L_${m.name}_2026.csv`; a.click(); URL.revokeObjectURL(url);
});
document.getElementById("exportPdf")?.addEventListener("click", async ()=>{
  const {jsPDF}=window.jspdf; const doc=new jsPDF();
  let m, p, revs, cogss, opexes;
  if(DATA_MODE==="sql"){
    if(!sqlPnlCache) await loadSqlPnl();
    const d=sqlPnlCache; m={name: sqlMonths[S.selectedMonth].month_name}; p={rev:d.pnl.total_revenue, cogs:d.pnl.total_cogs, gross:d.pnl.gross_profit, gm:d.pnl.gross_margin, opex:d.pnl.total_opex, op:d.pnl.operating_profit, net:d.pnl.net_profit, nm:d.pnl.net_margin, status:d.pnl.status}; revs=d.revenue; cogss=d.cogs; opexes=d.expenses;
    doc.setFontSize(16); doc.text(`P&L Statement - ${m.name} 2026 (SQL)`,14,16);
    doc.setFontSize(10); let y=24;
    doc.text("REVENUE",14,y); y+=6; revs.forEach(r=>{doc.text(`${r.source}`,14,y); doc.text(fmtPdf(r.amount),180,y,{align:"right"}); y+=6;});
    doc.setFont(undefined,'bold'); doc.text("TOTAL REVENUE",14,y); doc.text(fmtPdf(p.rev),180,y,{align:"right"}); y+=8; doc.setFont(undefined,'normal');
    doc.text("COGS",14,y); y+=6; cogss.forEach(c=>{doc.text(c.source,14,y); doc.text(fmtPdf(c.amount),180,y,{align:"right"}); y+=6;});
    doc.setFont(undefined,'bold'); doc.text("TOTAL COGS",14,y); doc.text(fmtPdf(p.cogs),180,y,{align:"right"}); y+=6;
    doc.text(`GROSS PROFIT ${fmtPdf(p.gross)} (${p.gm.toFixed(2)}%)`,14,y); y+=8; doc.setFont(undefined,'normal');
    doc.text("OPERATING EXPENSES",14,y); y+=6; opexes.forEach(o=>{doc.text(o.category,14,y); doc.text(fmtPdf(o.amount),180,y,{align:"right"}); y+=6;});
    doc.setFont(undefined,'bold'); doc.text("TOTAL OPEX",14,y); doc.text(fmtPdf(p.opex),180,y,{align:"right"}); y+=6;
    doc.text(`OPERATING PROFIT ${fmtPdf(p.op)}`,14,y); y+=6; doc.text(`NET ${p.status.toUpperCase()} ${fmtPdf(p.net)} (${p.nm.toFixed(2)}%)`,14,y);
    doc.save(`P&L_SQL_${m.name}_2026.pdf`); return;
  }
  m=cur(); p=pnl(m);
  doc.setFontSize(16); doc.text(`P&L Statement - ${m.name} 2026`,14,16);
  doc.setFontSize(10);
  let y=24;
  doc.text("REVENUE",14,y); y+=6; m.revenue.forEach(r=>{doc.text(`${r.source}`,14,y); doc.text(fmtPdf(r.amount),180,y,{align:"right"}); y+=6;});
  doc.setFont(undefined,'bold'); doc.text("TOTAL REVENUE",14,y); doc.text(fmtPdf(p.rev),180,y,{align:"right"}); y+=8; doc.setFont(undefined,'normal');
  doc.text("COGS",14,y); y+=6; m.cogs.forEach(c=>{doc.text(c.source,14,y); doc.text(fmtPdf(c.amount),180,y,{align:"right"}); y+=6;});
  doc.setFont(undefined,'bold'); doc.text("TOTAL COGS",14,y); doc.text(fmtPdf(p.cogs),180,y,{align:"right"}); y+=6;
  doc.text(`GROSS PROFIT ${fmtPdf(p.gross)} (${p.gm.toFixed(2)}%)`,14,y); y+=8; doc.setFont(undefined,'normal');
  doc.text("OPERATING EXPENSES",14,y); y+=6; m.opex.forEach(o=>{doc.text(o.category,14,y); doc.text(fmtPdf(o.amount),180,y,{align:"right"}); y+=6;});
  doc.setFont(undefined,'bold'); doc.text("TOTAL OPEX",14,y); doc.text(fmtPdf(p.opex),180,y,{align:"right"}); y+=6;
  doc.text(`OPERATING PROFIT ${fmtPdf(p.op)}`,14,y); y+=6; doc.text(`NET ${p.status.toUpperCase()} ${fmtPdf(p.net)} (${p.nm.toFixed(2)}%)`,14,y);
  doc.save(`P&L_${m.name}_2026.pdf`);
});
document.getElementById("exportAnnualCsv")?.addEventListener("click", async ()=>{
  if(DATA_MODE==="sql"){
    if(!sqlDashboard) await loadSqlDashboard();
    let csv="Month,Revenue,COGS,OPEX,Net Profit (SQL)\n"; sqlDashboard.monthly.forEach(m=>{csv+=`${m.month},${m.total_revenue},${m.total_cogs},${m.total_opex},${m.net_profit}\n`;});
    csv+=`ANNUAL,${sqlDashboard.yearly.annual_revenue},${sqlDashboard.yearly.annual_cogs},${sqlDashboard.yearly.annual_opex},${sqlDashboard.yearly.annual_net_profit}\n`;
    const blob=new Blob([csv],{type:"text/csv"}); const url=URL.createObjectURL(blob); const a=document.createElement("a"); a.href=url; a.download="Annual_Report_SQL_2026.csv"; a.click(); URL.revokeObjectURL(url); return;
  }
  let csv="Month,Revenue,COGS,OPEX,Net Profit\n"; S.months.forEach(m=>{const p=pnl(m); csv+=`${m.name},${p.rev},${p.cogs},${p.opex},${p.net}\n`;});
  const y=yearly(); csv+=`ANNUAL,${y.rev},${y.cogs},${y.opex},${y.net}\n`;
  const blob=new Blob([csv],{type:"text/csv"}); const url=URL.createObjectURL(blob); const a=document.createElement("a"); a.href=url; a.download="Annual_Report_2026.csv"; a.click(); URL.revokeObjectURL(url);
});

async function renderAll(){
  if(DATA_MODE==="sql"){
    if(!sqlMonths.length) await loadSqlMonths();
    if(!sqlDashboard) await loadSqlDashboard();
    await loadSqlPnl();
    fillMonthSel();
  } else if(DATA_MODE==="mongo"){
    if(!mongoMonths.length) await loadMongoMonths().catch(()=>{});
    if(!mongoDashboard) await loadMongoDashboard().catch(()=>{});
    await loadMongoPnl().catch(()=>{});
    if(mongoMonths.length) fillMonthSel();
  }
  await renderLists(); await renderDashboard(); renderYearlyReport(); await renderPnlTable(); await renderBreakEven(); renderSimulator(); await renderForecast(); setTimeout(renderCharts,50);
}

// --- v2 additions: multi-business, GST, CSV import, FY, branded PDF, audit ---
// CURRENT_BIZ already declared at top (with localStorage persistence)
if(typeof CURRENT_BIZ === 'undefined' || !CURRENT_BIZ) CURRENT_BIZ=1;
let GST_ON=false;
async function loadBusinesses(){
  try{
    const bizs=await apiGet("/api/businesses");
    const sel=document.getElementById("businessSelect");
    const top=document.getElementById("topBusinessName");
    if(sel){
      sel.innerHTML="";
      bizs.forEach(b=>{
        const o=document.createElement("option"); o.value=b.id; o.textContent=b.name; if(b.id===CURRENT_BIZ) o.selected=true; sel.appendChild(o);
      });
    }
    if(top) top.textContent = bizs.find(b=>b.id===CURRENT_BIZ)?.name || S.business;
    const remBtn=document.getElementById("removeBusinessBtn");
    if(remBtn){
      remBtn.disabled = bizs.length<=1;
      remBtn.style.opacity = bizs.length<=1 ? "0.5" : "1";
      remBtn.title = bizs.length<=1 ? "Cannot delete last business" : "Remove selected business";
    }
  }catch(e){ console.error("biz load",e); }
}
async function loadUsers(){
  try{
    const users=await apiGet("/api/users");
    const sel=document.getElementById("userSelect");
    if(sel){
      sel.innerHTML="";
      users.forEach(u=>{
        const o=document.createElement("option"); o.value=u.email; o.textContent=`${u.name} (${u.role})`; sel.appendChild(o);
      });
    }
  }catch(e){}
}
document.getElementById("businessSelect")?.addEventListener("change", async e=>{
  CURRENT_BIZ=parseInt(e.target.value);
  localStorage.setItem("current_biz", CURRENT_BIZ);
  sqlMonths=[]; sqlDashboard=null; sqlPnlCache=null; fyCache=null;
  await loadSqlMonths(); await loadSqlDashboard(); await loadSqlPnl();
  renderAll(); loadBusinesses(); loadFy(); loadAudit();
});
document.getElementById("addBusinessBtn")?.addEventListener("click", async ()=>{
  const name=prompt("New business name:");
  if(!name || !name.trim()) return;
  const btn=document.getElementById("addBusinessBtn");
  const orig=btn.textContent; btn.textContent="Creating..."; btn.disabled=true;
  try{
    const res=await apiPost("/api/businesses",{name:name.trim()});
    CURRENT_BIZ=res.id;
    localStorage.setItem("current_biz", CURRENT_BIZ);
    sqlMonths=[]; sqlDashboard=null; sqlPnlCache=null;
    await loadBusinesses();
    await loadSqlMonths(); await loadSqlDashboard(); await loadSqlPnl();
    // update top name
    const top=document.getElementById("topBusinessName");
    if(top) top.textContent=name.trim();
    document.getElementById("bizName").textContent=name.trim();
    renderAll(); loadFy();
    alert(`✓ Created "${name.trim()}" (ID ${res.id}) — switched to it`);
  }catch(e){ alert("Create failed: "+e.message); console.error(e); }
  finally{ btn.textContent=orig; btn.disabled=false; }
});
document.getElementById("removeBusinessBtn")?.addEventListener("click", async ()=>{
  const sel=document.getElementById("businessSelect");
  const bizId=parseInt(sel?.value);
  const bizName=sel?.options[sel.selectedIndex]?.textContent || "this business";
  if(!bizId){ alert("No business selected"); return; }
  try{
    const bizs=await apiGet("/api/businesses");
    if(bizs.length<=1){ alert("Cannot delete last business — at least one must remain. Create another first."); return; }
  }catch(e){ console.error(e); }
  if(!confirm(`Delete business "${bizName}" (ID ${bizId})?\nThis will permanently delete its 12 months, revenue, COGS & expenses. Cannot be undone.`)) return;
  const btn=document.getElementById("removeBusinessBtn");
  const orig=btn.textContent; btn.textContent="Removing..."; btn.disabled=true;
  try{
    await apiDel(`/api/businesses/${bizId}`);
    // switch to first remaining business
    const bizs=await apiGet("/api/businesses");
    CURRENT_BIZ=bizs[0]?.id || 1;
    localStorage.setItem("current_biz", CURRENT_BIZ);
    sqlMonths=[]; sqlDashboard=null; sqlPnlCache=null;
    mongoMonths=[]; mongoDashboard=null; mongoPnlCache=null;
    await loadBusinesses();
    try{ await loadSqlMonths(); await loadSqlDashboard(); await loadSqlPnl(); }catch(e){}
    try{ await loadMongoMonths(); await loadMongoDashboard(); await loadMongoPnl(); }catch(e){}
    renderAll(); loadFy();
    alert(`✓ Removed "${bizName}" (ID ${bizId}) — switched to ${bizs[0]?.name || "remaining business"}`);
  }catch(e){ alert("Delete failed: "+e.message); console.error(e); }
  finally{ btn.textContent=orig; btn.disabled=false; }
});
document.getElementById("gstToggle")?.addEventListener("change", e=>{
  GST_ON=e.target.checked; renderAll();
});
function applyGst(amount){
  if(!GST_ON) return amount;
  return Math.round(amount * 1.18);
}
document.getElementById("csvFile")?.addEventListener("change", async e=>{
  const file=e.target.files[0]; if(!file) return;
  const text=await file.text();
  const lines=text.trim().split(/\r?\n/);
  const rows=[];
  for(let i=1;i<lines.length;i++){
    const cols=lines[i].split(",");
    if(cols.length<3) continue;
    const type=(cols[0]||"revenue").trim().toLowerCase(); // revenue/cogs/expense
    const source=cols[1].trim();
    const amount=toNumber(cols[2]);
    if(!source || isNaN(amount)) continue;
    rows.push({type, source, amount});
  }
  if(!rows.length){ alert("CSV format: type,source,amount\nExample: revenue,Subscription,10000"); return; }
  const mid=curMonthId() || 9;
  try{
    if(DATA_MODE==="sql"){
      const res=await apiPost("/api/import",{business_id:CURRENT_BIZ, month_id:mid, rows});
      alert(`Imported ${res.imported} rows to SQL (month ${mid})`);
      await loadSqlPnl(); await loadSqlDashboard();
    } else {
      const m=cur();
      rows.forEach(r=>{
        if(r.type==="revenue") m.revenue.push({id:Date.now()+Math.random(), source:r.source, amount:r.amount});
        else if(r.type==="cogs") m.cogs.push({id:Date.now()+Math.random(), source:r.source, amount:r.amount});
        else m.opex.push({id:Date.now()+Math.random(), category:r.source, amount:r.amount});
      });
      save(); alert(`Imported ${rows.length} rows locally`);
    }
    renderAll();
  }catch(err){ alert("Import failed: "+err.message); }
  e.target.value="";
});
let fyCache=null;
function calcMovingAvg(values, window=3){
  const out=[];
  for(let i=0;i<values.length;i++){
    const w=values.slice(Math.max(0,i-window+1), i+1);
    out.push(Math.round(w.reduce((a,b)=>a+b,0)/w.length*100)/100);
  }
  return out;
}
function calcAnomalies(values){
  if(values.length<3) return values.map((v,i)=>({index:i, value:v, z:0, anomaly:false}));
  const mean=values.reduce((a,b)=>a+b,0)/values.length;
  const variance=values.reduce((a,b)=>a+(b-mean)**2,0)/values.length;
  const std=Math.sqrt(variance);
  return values.map((v,i)=>({index:i, value:v, z: std? Math.round((v-mean)/std*100)/100:0, anomaly: std? Math.abs((v-mean)/std)>2:false}));
}
function renderYearlyReport(fyOverride){
  try{
    let y=null, fy=null, anomalies=[], ma=[];
    let modeLabel = DATA_MODE==="sql" ? "SQL" : DATA_MODE==="mongo" ? "MongoDB" : "Local";
    if(fyOverride){ fyCache=fyOverride; }
    if(DATA_MODE==="sql" && sqlDashboard){
      y=sqlDashboard.yearly;
      if(fyCache) { fy=fyCache.fy; anomalies=fyCache.anomalies; ma=fyCache.moving_avg_revenue; }
      else if(fyOverride){ fy=fyOverride.fy; anomalies=fyOverride.anomalies||[]; ma=fyOverride.moving_avg_revenue||[]; }
    } else if(DATA_MODE==="mongo" && mongoDashboard){
      y=mongoDashboard.yearly;
      if(fyCache) { fy=fyCache.fy; anomalies=fyCache.anomalies; ma=fyCache.moving_avg_revenue; }
    } else {
      const yl=yearly();
      y={annual_revenue:yl.rev, annual_cogs:yl.cogs, annual_gross_profit:yl.gross, annual_gross_margin:yl.gm, annual_opex:yl.opex, annual_net_profit:yl.net, annual_net_margin:yl.nm};
      // FY Apr-Mar reorder
      const pnls=S.months.map(m=>pnl(m));
      const fyPnls=pnls.slice(3).concat(pnls.slice(0,3));
      let fyRev=0,fyCogs=0,fyOpex=0;
      fyPnls.forEach(p=>{fyRev+=p.rev; fyCogs+=p.cogs; fyOpex+=p.opex;});
      const fyGross=fyRev-fyCogs; const fyGm=fyRev?fyGross/fyRev*100:0; const fyOp=fyGross-fyOpex; const fyNet=fyOp; const fyNm=fyRev?fyNet/fyRev*100:0;
      fy={annual_revenue:Math.round(fyRev*100)/100, annual_cogs:Math.round(fyCogs*100)/100, annual_gross_profit:Math.round(fyGross*100)/100, annual_opex:Math.round(fyOpex*100)/100, annual_net_profit:Math.round(fyNet*100)/100, annual_gross_margin:Math.round(fyGm*100)/100, annual_net_margin:Math.round(fyNm*100)/100};
      anomalies=calcAnomalies(pnls.map(p=>p.net));
      ma=calcMovingAvg(pnls.map(p=>p.rev),3);
      fyCache={fy, anomalies, moving_avg_revenue:ma};
    }
    // fallback if y still null (e.g., sqlDashboard not loaded yet but local fallback)
    if(!y){
      const yl=yearly();
      y={annual_revenue:yl.rev, annual_cogs:yl.cogs, annual_gross_profit:yl.gross, annual_gross_margin:yl.gm, annual_opex:yl.opex, annual_net_profit:yl.net, annual_net_margin:yl.nm};
    }
    if(!fy && fyCache) { fy=fyCache.fy; anomalies=fyCache.anomalies||[]; ma=fyCache.moving_avg_revenue||[]; }
    // badge & label (dashboard FY summary)
    const badge=document.getElementById("fyBadge");
    const label=document.getElementById("fyLabel");
    if(badge && fy) badge.textContent=`FY Apr-Mar Net ${fmt(fy.annual_net_profit)} • ${modeLabel}`;
    if(label && fy && ma && ma.length) label.textContent=`• FY Apr-Mar Net ${fmt(fy.annual_net_profit)} • MA(3) rev ${fmt(ma[ma.length-1])}`;
    // anomaly & moving avg
    const alertEl=document.getElementById("anomalyAlert");
    if(alertEl){
      if(anomalies && anomalies.some(a=>a.anomaly)){
        alertEl.style.display="inline"; alertEl.textContent=`\u26A0 ${anomalies.filter(a=>a.anomaly).length} anomaly months detected`;
      } else { alertEl.style.display="none"; alertEl.textContent=""; }
    }
    const maEl=document.getElementById("maLine");
    if(maEl && ma) maEl.textContent=`3-mo moving avg revenue: ${ma.map(v=>fmt(v)).join(" \u2192 ")}`;
    // Yearly Report page: yearlyCards2 -> annual summary (5 KPIs same as dashboard)
    const y2=document.getElementById("yearlyCards2");
    if(y2 && y){
      y2.innerHTML=`
        <div class="card"><h3 style="font-size:12px;color:#64748b">Annual Revenue</h3><div style="font-size:20px;font-weight:800">${fmt(y.annual_revenue)}</div><div style="font-size:11px;color:#64748b">${modeLabel} • Calendar Jan-Dec 2026</div></div>
        <div class="card"><h3 style="font-size:12px;color:#64748b">Annual COGS</h3><div style="font-size:20px;font-weight:800">${fmt(y.annual_cogs)}</div><div style="font-size:11px;color:#64748b">${y.annual_revenue? (y.annual_cogs/y.annual_revenue*100).toFixed(1):0}% of revenue</div></div>
        <div class="card"><h3 style="font-size:12px;color:#64748b">Annual Gross Profit</h3><div style="font-size:20px;font-weight:800;color:#10b981">${fmt(y.annual_gross_profit)} \u00B7 ${Number(y.annual_gross_margin).toFixed(1)}%</div></div>
        <div class="card"><h3 style="font-size:12px;color:#64748b">Annual OPEX</h3><div style="font-size:20px;font-weight:800">${fmt(y.annual_opex)}</div></div>
        <div class="card" style="border:2px solid ${y.annual_net_profit>=0?'#10b981':'#ef4444'}"><h3 style="font-size:12px;color:#64748b">Annual Net ${y.annual_net_profit>=0?'Profit':'Loss'}</h3><div style="font-size:20px;font-weight:800;color:${y.annual_net_profit>=0?'#10b981':'#ef4444'}">${fmt(y.annual_net_profit)} \u00B7 ${Number(y.annual_net_margin).toFixed(1)}%</div></div>
      `;
    }
    // FY card
    const fyEl=document.getElementById("fyCards");
    if(fyEl && fy){
      const an=anomalies? anomalies.filter(a=>a.anomaly):[];
      fyEl.innerHTML=`<div class="card" style="background:#fefce8;border-color:#fde68a"><h3 style="font-size:11px;color:#92400e">FY Apr-Mar (India) \u2022 ${modeLabel} \u2022 GST ${GST_ON?"18% ON":"off"}</h3><div style="font-size:14px;font-weight:700">Revenue ${fmt(fy.annual_revenue)} \u2192 Net ${fmt(fy.annual_net_profit)} (${Number(fy.annual_net_margin).toFixed(1)}%)</div><div style="font-size:11px;color:#64748b">Gross ${fmt(fy.annual_gross_profit)} (${Number(fy.annual_gross_margin).toFixed(1)}%) \u2022 OPEX ${fmt(fy.annual_opex)} \u2022 Anomalies: ${an.length? an.map(a=>`M${a.index+1} z=${a.z}`).join(", ") : "none"}</div><div style="font-size:11px;color:#64748b;margin-top:4px">FY = Apr 2026-Mar 2026 reordered; Calendar = Jan-Dec</div></div>`;
    }
    // also add monthly breakdown table into Yearly Report if container exists
    let breakdown=document.getElementById("yearlyBreakdown");
    if(!breakdown && y2){
      breakdown=document.createElement("div");
      breakdown.id="yearlyBreakdown";
      breakdown.style.marginTop="12px";
      y2.parentElement.appendChild(breakdown);
    }
    if(breakdown){
      let rows=[];
      if(DATA_MODE==="sql" && sqlDashboard) rows=sqlDashboard.monthly;
      else if(DATA_MODE==="mongo" && mongoDashboard) rows=mongoDashboard.monthly;
      else rows=S.months.map(m=>{const p=pnl(m); return {month:m.name, total_revenue:p.rev, total_cogs:p.cogs, total_opex:p.opex, net_profit:p.net, gross_margin:p.gm, net_margin:p.nm}});
      breakdown.innerHTML=`<div style="overflow:auto"><table class="table" style="margin-top:8px;font-size:12px"><thead><tr><th>Month</th><th style="text-align:right">Revenue</th><th style="text-align:right">COGS</th><th style="text-align:right">OPEX</th><th style="text-align:right">Net</th><th style="text-align:right">Margin</th></tr></thead><tbody>${rows.map(r=>`<tr><td>${r.month}</td><td style="text-align:right">${fmt(r.total_revenue)}</td><td style="text-align:right">${fmt(r.total_cogs)}</td><td style="text-align:right">${fmt(r.total_opex)}</td><td style="text-align:right;color:${r.net_profit>=0?'#10b981':'#ef4444'};font-weight:700">${fmt(r.net_profit)}</td><td style="text-align:right">${Number(r.net_margin||0).toFixed(1)}%</td></tr>`).join("")}</tbody><tfoot><tr class="pl-total"><td>ANNUAL</td><td style="text-align:right">${fmt(y.annual_revenue)}</td><td style="text-align:right">${fmt(y.annual_cogs)}</td><td style="text-align:right">${fmt(y.annual_opex)}</td><td style="text-align:right">${fmt(y.annual_net_profit)}</td><td style="text-align:right">${Number(y.annual_net_margin).toFixed(1)}%</td></tr></tfoot></table></div><div style="font-size:11px;color:#64748b;margin-top:6px">* ${modeLabel} mode \u2022 Calculated via ${DATA_MODE==="local"?"browser (yearly())": "backend/calculations.py"} \u2022 FY Apr-Mar reorders calendar for India fiscal year</div>`;
    }
  }catch(e){ console.error("renderYearlyReport",e); }
}
async function loadFy(){
  try{
    const fy=await apiGet(`/api/fy/${CURRENT_BIZ}`);
    fyCache=fy;
    renderYearlyReport(fy);
  }catch(e){
    console.warn("fy API failed, falling back to local calc",e);
    renderYearlyReport(null);
  }
}
document.getElementById("exportFyCsv")?.addEventListener("click", async ()=>{
  try{
    const fy=await apiGet(`/api/fy/${CURRENT_BIZ}`);
    let csv="FY Apr-Mar,Revenue,Net Profit\n"; csv+=`FY Total,${fy.fy.annual_revenue},${fy.fy.annual_net_profit}\n`;
    const blob=new Blob([csv],{type:"text/csv"}); const url=URL.createObjectURL(blob); const a=document.createElement("a"); a.href=url; a.download="FY_Report.csv"; a.click();
  }catch(e){
    // Local fallback
    const pnls=S.months.map(m=>pnl(m));
    const fyPnls=pnls.slice(3).concat(pnls.slice(0,3));
    let fyRev=0,fyCogs=0,fyOpex=0;
    fyPnls.forEach(p=>{fyRev+=p.rev; fyCogs+=p.cogs; fyOpex+=p.opex;});
    const fyNet=fyRev-fyCogs-fyOpex;
    let csv="FY Apr-Mar,Revenue,Net Profit (Local)\n"; csv+=`FY Total,${fyRev},${fyNet}\n`;
    const blob=new Blob([csv],{type:"text/csv"}); const url=URL.createObjectURL(blob); const a=document.createElement("a"); a.href=url; a.download="FY_Report_Local.csv"; a.click();
  }
});
// patch api helpers to use CURRENT_BIZ (now handles mongo too via main curMonthId)
const _origCurMonthId = curMonthId;
curMonthId = function(){ if(DATA_MODE==="mongo" && mongoMonths.length) return mongoMonths[S.selectedMonth]?.id; if(DATA_MODE==="sql" && sqlMonths.length) return sqlMonths[S.selectedMonth]?.id; return null; };
// branded PDF override: add header
const _origExport = document.getElementById("exportPdf")?.onclick;
document.getElementById("exportPdf")?.addEventListener("click", async ()=>{}, {once:true}); // ensure branded pdf uses existing handler but with business name
// audit log
async function loadAudit(){
  try{
    const logs=await apiGet(`/api/audit?business_id=${CURRENT_BIZ}`);
    const el=document.getElementById("auditLog");
    if(el){
      if(logs.length) el.innerHTML=`<h4 style="font-size:11px;color:#64748b">Audit (last 5) • ${DATA_MODE}</h4>`+logs.slice(0,5).map(l=>`<div style="padding:4px 0;border-bottom:1px solid #e2e8f0">${l.action} — ${l.details||""} <span style="color:#94a3b8">${l.created_at}</span></div>`).join("");
      else el.innerHTML=`<h4 style="font-size:11px;color:#64748b">Audit (last 5)</h4><div style="color:#94a3b8;padding:8px 0">No audit entries yet — logs appear after creates/deletes via API.</div>`;
    }
  }catch(e){
    const el=document.getElementById("auditLog");
    if(el) el.innerHTML=`<h4 style="font-size:11px;color:#64748b">Audit (Local mode)</h4><div style="color:#94a3b8;padding:8px 0">Audit requires Flask :5000 SQL connection. Switch to SQL mode or start backend.</div>`;
  }
}

// init v2
(async()=>{
  if(DATA_MODE==="sql"){
    await loadSqlMonths();
    await loadSqlDashboard();
    await loadSqlPnl();
  } else if(DATA_MODE==="mongo"){
    await loadMongoMonths().catch(()=>{});
    await loadMongoDashboard().catch(()=>{});
    await loadMongoPnl().catch(()=>{});
  }
  fillMonthSel(); renderAll();
  loadBusinesses(); loadUsers(); loadFy(); loadAudit();
})();
