.PHONY: ftn_joint_scrape ftn_joint_history ftn_perso_scrape guess_category

ftn_joint_scrape:
	docker exec -it python python main.py ftn_joint_scrape $(INTERVAL)

ftn_joint_history:
	docker exec -it python python main.py ftn_joint_history

ftn_perso_scrape:
	docker exec -it python python main.py ftn_perso_scrape $(INTERVAL)

guess_category:
	docker exec -it python python main.py guess_category

# If INTERVAL is not provided, set it to default value 1
INTERVAL ?= 1