#!/bin/bash
# Write the spreadsheets to the json.
declare -a SHEETS=('base-unemployment' 'monthly-job-creation' 'labor-participation-rate' 'year-over-year-wage-growth' 'gdp-growth' 'african-american-unemployment' 'manufacturing-jobs' 'coal-mining-jobs' 'uninsured-rate' 'us-trade-deficit' 'total-outstanding-debt' 'americans-on-food-stamps')
DIR='www/_output'
ALL="$DIR/all.js"

# Write the latest to individual json files, as well as one giant js file with assigned var names.
echo "var data = { " > $ALL;
for SHEET in ${SHEETS[@]}; do
    python readwritesheet.py $SHEET
    SLUG=${SHEET//-/_}
    echo "     $SLUG: `cat $DIR/$SHEET.json`," >> $ALL
done

# Append a list of the sheet-to-variable names to the end of the all.js
echo "    all: [" >> $ALL
for SHEET in ${SHEETS[@]}; do
    SLUG=${SHEET//-/_}
    echo "'$SLUG'," >> $ALL
done
echo "]};" >> $ALL
