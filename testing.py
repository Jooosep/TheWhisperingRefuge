CREATE USER "dbuser"@"localhost" IDENTIFIED BY "dbpass";
GRANT SELECT, INSERT, UPDATE, DElete ON whispertest.* TO dbuser@localhost;
