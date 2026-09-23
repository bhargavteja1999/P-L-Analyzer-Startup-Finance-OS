-- 01_create_database.sql
-- Database Initialization & Configuration Script for AI-Expense-Sales-Analyzer
-- Creates the logical database container and configures session parameters.

-- Enable foreign keys constraint enforcement (SQLite / ANSI SQL)
PRAGMA foreign_keys = ON;

-- Configure database encoding and WAL mode for high performance
PRAGMA encoding = "UTF-8";
PRAGMA journal_mode = WAL;

SELECT 'Database expense_sales successfully initialized.' AS Status;
