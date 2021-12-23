# once python identifies that a specific addon needs updating, it passes the
# url to the download info page to this script which does the dirty work.

echo "Installing" from $1

# download the info page
wget -q $1

# now extract download link from download page...
download_link=$(cat *.html | grep -oP '(?<=href=\").*?(?=\">Click here)')

# perform the download
wget -O temp.zip -q $download_link

# unzip the update.. -u forces to replace old folders and add new ones if necessary
unzip -uoq *.zip

# cleanup
rm *.html *.zip

