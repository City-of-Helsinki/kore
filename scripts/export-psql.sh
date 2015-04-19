#!/bin/bash

ACC_FILE=kore_tietokanta_ta.accdb
DB=test

mdb-schema $ACC_FILE postgres > schema.sql
cat schema.sql | grep -v CONSTRAINT | grep -v INDEX | psql -q $DB

rm -f bool-columns.txt

echo Sniffing out boolean columns
for t in $(mdb-tables $ACC_FILE) ; do
	for c in $(echo \\d \"$t\" | psql $DB | grep boolean| cut -d '|' -f 1) ; do
		echo $t $c >> bool-columns.txt
	done
done

echo Changing boolean columns to integers
while read -r t c; do
	echo "ALTER TABLE \"$t\" ALTER COLUMN $c TYPE int USING 0;" | psql -q $DB
done < bool-columns.txt

for t in $(mdb-tables $ACC_FILE) ; do
	echo Exporting $t
	mdb-export -I postgres -b strip -q \' $ACC_FILE $t | psql -q $DB
done

echo Creating constraints and indices
cat schema.sql | grep -e CONSTRAINT -e INDEX | psql -q $DB
rm schema.sql

echo Changing columns back to booleans
while read -r t c; do
	echo "ALTER TABLE \"$t\" ALTER COLUMN $c TYPE boolean USING CASE WHEN $c=0 THEN FALSE ELSE TRUE END;" | psql -q $DB
done < bool-columns.txt

rm bool-columns.txt

echo Creating fake primary keys
SQL="
ALTER TABLE \"Rakennuksen_status\" ADD COLUMN id VARCHAR;
UPDATE \"Rakennuksen_status\" SET id = koulun_id || '-' || rakennuksen_id;
ALTER TABLE \"Rakennuksen_status\" DROP CONSTRAINT IF EXISTS \"Rakennuksen_status_pkey\";
ALTER TABLE \"Rakennuksen_status\" ADD PRIMARY KEY (id);
"

psql -q $DB -c "$SQL"

for t in $(psql -c "\di" $DB | grep _pkey | cut -d '|' -f 2 | sed -e 's/_pkey//') ; do
	echo "ALTER TABLE \"$t\" ADD COLUMN id SERIAL;" | psql -q $DB
done
