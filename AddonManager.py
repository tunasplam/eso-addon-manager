# our addon manager...
# Keeps a list of the urls of the ESOUI pages for our addons...
# Can also install addons using this... and that is recommended because
# it will update our list of urls.

# TODO Functionality to remove addons..
# For now.. do manually. Delete folder and remove entry from text file.
import os
import datetime
import re
import sys

def main():
	if "-i" in sys.argv:
		print("Installing Addon:\n")
		# get the url... send to install.
		url_index = sys.argv.index("-i") + 1
		try:
			install_addon(sys.argv[url_index])
		except IndexError:
			help("ERROR. Did you forget to include the URL?")
		print("Done!")

	elif "-u" in sys.argv:
		print("Updating Addons:\n")
		check_for_updates()
		print("Done!")

	else:
		help()

	# Backup the text file.
	backup_command = "cp ESOUIurls.txt ESOUIurlsBU.txt"

# Print error message (if applicable), proper usage, then bail
def help(error_message=""):
	print(error_message + "\n")
	print("ESO Addon Manager")
	print("usage:")
	print("python AddonManager.py [args]")
	print("-u update")
	print("-i [url] need to use INFO PAGE from ESOUI for desired addon")
	sys.exit()

# list of urls for downloaded addons
# returns list of strings.. one for each url
def get_url_list():
	urls_file = open("ESOUIurls.txt")
	urls = urls_file.read()
	urls_file.close()
	return urls.split("\n")

# wgets the http page for a given esoui addon
# needs to convert it form ISO-8859-14 to UTF-8 for python
def download_addon_url(url):
	# wget the url.
	os.system("wget -q " + url)

	# converts file name to output of wget
	url = url[32:]
	print(url)

	# convert the file to UTF-8
	os.system("iconv -f ISO8859-14 -t UTF-8 " + url + " -o " + url)

	# open the file and grab the contents
	# May throw file not found if url is incorrect in text file...
	try:
		addon_url_file = open(url)
		addon_file = addon_url_file.read()
		addon_url_file.close()
	except FileNotFoundError:
		end_gracefully("URL in text file possibly invalid... Ending gracefullly.")

	cleanup()

	return addon_file


# ONLY NEEDED TO BE RUN ONCE. AND IT HAS BEEN RUN!
# This is run on setup.. populates updated times for currently existing UI addons.
# will rewrite the old file in doing so.
def populate_updated():
	# gets the list of the ESOUI addon page urls
	urls = get_url_list()
	# opens the old esoui info file for editing.
	urls_file = open("ESOUIurls_temp.txt", 'a')
	for addon in urls:
		# grab the url with regex. if index error then at end of list( TODO FIX THIS )
		try:
			url = re.findall(r'(?<=<url>).*(?=</url>)', addon)[0]
		except IndexError:
			break

		# download the file
		addon_file = download_addon_url(url)

		date_last_updated = re.findall(r'(?<=Updated: ).*?(?= )', addon_file)[0]
		print(date_last_updated)

		# now need to replace the last empty last updated entry with the date found.
		addon += ("<updated>" + date_last_updated + "</updated></addon>")
		urls_file.write(addon + "\n")
	urls_file.close()

	# replace old file with temp file.
	rm_mv_command = "rm ESOUIurls.txt && mv ESOUIurls_temp.txt ESOUIurls.txt"
	os.system(rm_mv_command)

# Checks for updates.. if updates are needed then updates.
def check_for_updates():
	# starts out by getting the url list
	urls = get_url_list()

	# creates temp eosuiurl file to edit...
	urls_file = open("ESOUIurls_temp.txt", 'a')

	# Now... cycles through the list of urls and checks the date_last_updated page
	for addon_info in urls:
		# grab the url with regex. if index error then at end of list( TODO FIX THIS )
		try:
			url = re.findall(r'(?<=<url>).*(?=</url>)', addon_info)[0]
		except IndexError:
			break

		# download the file
		addon_file = download_addon_url(url)

		# this is the date that the mod admin updated the mod on esoui
		date_esoui_last_updated = re.findall(r'(?<=Updated: ).*?(?= )', addon_file)[0]

		# check against the date in the our addon_file...
		date_last_updated = re.findall(r'(?<=<updated>).*(?=</updated>)', addon_info)[0]
		# converts to python datetime objects and compares.
		dt_date_last_updated = datetime.datetime(year=int(date_last_updated[6:8]),
												 month=int(date_last_updated[0:2]),
												 day=int(date_last_updated[3:5]))
		dt_date_esoui_last_updated = datetime.datetime(year=int(date_esoui_last_updated[6:8]),
												       month=int(date_esoui_last_updated[0:2]),
												       day=int(date_esoui_last_updated[3:5]))
		if dt_date_last_updated < dt_date_esoui_last_updated:
			print("Need to update:")
			print(url)
			# Now pass url to the updater..
			download_addon(url)

			# Now we need to update the date_last_updated info
			today = datetime.date.today()
			addon_info = addon_info.replace(date_last_updated, today.strftime("%m/%d/%y"))
			urls_file.write(addon_info + "\n")

		# No need for update.... update text file and move on.
		else:
			urls_file.write(addon_info + "\n")

	urls_file.close()
	backup_text_file()

# installs given addon. url is for esoui info page.
def install_addon(url):
	new_addon_line = "<addon><url>" + url + "</url><updated>" + \
						datetime.date.today().strftime("%m/%d/%y") + "</updated></addon>\n"

	# download and install
	download_addon(url)

	# update the text file.
	urls_file = open("ESOUIurls.txt", 'a')
	urls_file.write(new_addon_line)
	urls_file.close()

def end_gracefully(message=""):
	print(message)
	cleanup()
	sys.exit()

# downloads addon with the given url
def download_addon(url):
	os.system("./update.sh " + url.replace("info", "download"))

# Make new backup ESOUIurls.txt
def backup_text_file():
	os.system("rm ESOUIurls.txt && mv ESOUIurls_temp.txt ESOUIurls.txt")

# cleanup html files
def cleanup():
	os.system("rm *.html")

main()