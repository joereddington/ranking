DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd $DIR
rm $DIR/sources/*
cd sources
while read -r url; do 
 wget -O "${url##http://}" "http://www.alexa.com/siteinfo/$url"
done < ../list_of_sources.txt
