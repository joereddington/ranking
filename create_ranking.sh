DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
DESTINATION_PAGE=/home/joereddington/joereddington.com/rankingProd.html
cd $DIR
rm $DIR/sources/*
cd sources
while read -r url; do 
 wget -O "${url##http://}" "http://www.alexa.com/siteinfo/$url"
 sleep 5
done < ../list_of_sources.txt

cat $DIR/start.html > $DESTINATION_PAGE 
grep -o -h "\"[^\"]*ranked number.*\"" * | sed 's/\"//g'  |  sed 's/\(^.*\) is ranked number\(.*\) in the.*/<\/td><td><a href=\"http:\/\/\1\">\1<\/a><\/td><td>\2<\/td><td><\/td><\/tr>/' > thelist.txt 
cat thelist.txt | sort -n -k 3 | head -n 60 > thelist2.txt
cat thelist2.txt | nl | sed 's/^/<tr><td>/g' >> $DESTINATION_PAGE
echo "</table><br> Ranking last updated at: " >> $DESTINATION_PAGE
date >> $DESTINATION_PAGE
cat $DIR/end.html >> $DESTINATION_PAGE
