DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
DESTINATION_PAGE=/home/joereddington/joereddington.com/rankingProdTest.html
cd $DIR
wget http://s3.amazonaws.com/alexa-static/top-1m.csv.zip
unzip top-1m.csv.zip
rm list1.txt
while read -r url; do 
 grep -m 1 "$url" top-1m.csv >> list1.txt
 echo grep "$url" top-1m.csv
done < list_of_sources.txt

cat $DIR/start.html > $DESTINATION_PAGE 
cat list1.txt | sort -n | head -n 60 |  sed 's/\(^[0-9]*\),\(.*\)/<\/td><td><a href=\"http:\/\/\2\">\2<\/a><\/td><td> \1 <\/td><td><\/td><\/tr>/' > list2.txt 
cat list2.txt | nl | sed 's/^/<tr><td>/g' >> $DESTINATION_PAGE
echo "</table><br> Ranking last updated at: " >> $DESTINATION_PAGE
date >> $DESTINATION_PAGE
cat $DIR/end.html >> $DESTINATION_PAGE
#rm top-1m.*
#rm list1.txt
#rm list2.txt
