query = shanghai chengdu 2017-01-15
start: install search
	echo "=================Dang Dang Dang====================="
search: stations.py
	./tickets.py $(query)
install:
	sudo pip3 install requests prettytable docopt
stations.py: parse_stations.py getStations.sh 
	./getStations.sh
clean:
	sudo rm -r __pycache__ ;
