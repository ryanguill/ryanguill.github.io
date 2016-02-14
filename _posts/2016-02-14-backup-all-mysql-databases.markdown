---
layout: post
title:  "Backup all MSSQL user databases"
date:   2016-02-14 12:00:00
author: Ryan Guill
categories: mssql sql
tags:	mssql sql
---

At my previous job we had several projects where we worked with MSSQL express, maybe with multiple databases.  Here is a quick script to just backup all user (non-system) databases on the system, quickly and easily.  It could probably be improved a bit, maybe better naming for the backups, but as a quick backup-all-the-things it works great.

<!-- break -->

{% highlight sql %}
DECLARE @name VARCHAR(50) -- database name  
DECLARE @path VARCHAR(256) -- path for backup files  
DECLARE @fileName VARCHAR(256) -- filename for backup  
DECLARE @fileDate VARCHAR(20) -- used for file name


-- specify database backup directory
SET @path = 'C:\DBBackups\'


-- specify filename format
SELECT @fileDate = CONVERT(VARCHAR(20),GETDATE(),112) + '-' + REPLACE(CONVERT(VARCHAR(20),GETDATE(),108),':','')


DECLARE db_cursor CURSOR FOR  
SELECT name
FROM master.dbo.sysdatabases  
WHERE name NOT IN ('master','model','msdb','tempdb')  -- exclude these databases


OPEN db_cursor   
FETCH NEXT FROM db_cursor INTO @name   


WHILE @@FETCH_STATUS = 0   
BEGIN   
       SET @fileName = @path + @name + '_' + @fileDate + '.BAK'  
       BACKUP DATABASE @name TO DISK = @fileName  


       FETCH NEXT FROM db_cursor INTO @name   
END   


CLOSE db_cursor   
DEALLOCATE db_cursorDECLARE @name VARCHAR(50) -- database name  
DECLARE @path VARCHAR(256) -- path for backup files  
DECLARE @fileName VARCHAR(256) -- filename for backup  
DECLARE @fileDate VARCHAR(20) -- used for file name


-- specify database backup directory
SET @path = 'C:\DBBackups\'


-- specify filename format
SELECT @fileDate = CONVERT(VARCHAR(20),GETDATE(),112) + '-' + REPLACE(CONVERT(VARCHAR(20),GETDATE(),108),':','')


DECLARE db_cursor CURSOR FOR  
SELECT name
FROM master.dbo.sysdatabases  
WHERE name NOT IN ('master','model','msdb','tempdb')  -- exclude these databases


OPEN db_cursor   
FETCH NEXT FROM db_cursor INTO @name   


WHILE @@FETCH_STATUS = 0   
BEGIN   
       SET @fileName = @path + @name + '_' + @fileDate + '.BAK'  
       BACKUP DATABASE @name TO DISK = @fileName  


       FETCH NEXT FROM db_cursor INTO @name   
END   


CLOSE db_cursor   
DEALLOCATE db_cursor
{% endhighlight %}
