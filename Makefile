clean:
	@echo "Cleaning up build and *.pyc files..."
	@find . -name '*.pyc' -exec rm -rf {} \;
	@rm -rf build

db: drop_db create_db migrate_db

db_test:
	@make drop_db create_db migrate_db migrate_db_down
	@make migrate_db
    
drop_db:
	@echo -n $(red)
	@echo "Dropping database..."
	@echo -n $(white)
	@mysql -u root -e 'DROP DATABASE IF EXISTS nginx_monitor;'
	@echo -n $(normal)

create_db:
	@echo "Creating database..."
	@echo -n $(white)
	@mysql -u root -e 'CREATE DATABASE IF NOT EXISTS nginx_monitor;'
	@echo -n $(green)
	@echo 'Database `nginx_monitor` created!'
	@echo -n $(normal)

migrate_db:
	@echo "Migrating nginx_monitor"
	@echo -n $(white)
	@db-migrate -c migrations/local.conf
	@echo -n $(green)
	@echo "Database migrated!"
	@echo -n $(green)
	@echo "DONE"
	@echo -n $(normal)

migrate_db_down:
	@echo "Migrating down to test migrations..."
	@echo -n $(white)
	@db-migrate -c migrations/local.conf -m 20091022185400
	@echo -n $(green)
	@echo "DONE"
	@echo -n $(normal)
	
start:
	@echo "Running nginx-monitor-server http://localhost:8080..."
	@cd nmonitor && python start.py start
