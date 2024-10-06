.PHONY: ftn_joint_scrape ftn_joint_history ftn_perso_scrape guess_category start stop

ftn_joint_scrape:
	docker exec -it python python main.py ftn_joint_scrape $(INTERVAL)

ftn_joint_history:
	docker exec -it python python main.py ftn_joint_history

ftn_perso_scrape:
	docker exec -it python python main.py ftn_perso_scrape $(INTERVAL)

ftn_perso_history:
	docker exec -it python python main.py ftn_perso_history

guess_category:
	docker exec -it python python main.py guess_category

cntrl_scrape_corolla:
	docker exec -it python python main.py cntrl_scrape_corolla

sptc_scrape_corolla:
	docker exec -it python python main.py sptc_scrape_corolla

start:
	docker compose up -d

stop:
	docker compose down --remove-orphans

# If INTERVAL is not provided, set it to default value 1
INTERVAL ?= 1