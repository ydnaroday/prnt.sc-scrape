#
# prntsc-scrape.py - get random images from the website https://prnt.sc/
#
# Andrew Rodriguez
# Friday May 15th, 2020
#

# Imports 
import os 	# I/O
import string 	# Some constants for generation.
import random 	# For random string.
import sys 	# Command line arguments.
import time 	# Check time.
import requests # Using get.
import bs4	# Easy html parsing.

#
# Code
#

# Create a random string of characters to append to the url.
def generate_string(length = 6):
	options = string.ascii_lowercase + string.digits

	return "".join(random.choices(options, k=length))

# Get a random image and save it.
def get_image():

	# Generate random url.
	url = "https://prnt.sc/"
	img_append = generate_string()
	print("Current url: " + url + img_append, end=" ")
	
	# Get initial website.
	# Here is a template for changing the agent.
	# "User-agent": "Mozilla/<version> (<system-information>) <platform> (<platform-details>) <extensions>"
	headers = {"User-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0"}
	html = requests.get(url + img_append, headers = headers).text
	soup = bs4.BeautifulSoup(html, "html.parser")

	# Get image website.
	image_url = soup.img["src"]
	if not image_url.startswith("http"):
		return False
	image = requests.get(image_url, headers = headers)

	# Save the image.
	file_location = "images/" + img_append + ".png"
	open(file_location, 'wb').write(image.content)

	return True

# Will check and create the needed directory.
def check_dir():
	if not os.path.exists("images"):
		os.mkdir("images")


# Main code.
def main():
	print("*** prnt.sc scrape ***")

	# Make sure directory exists.
	check_dir()

	# Amount of images to save.
	images = 1

	# Amount of fails.
	fails = 0

	# Check if user wants different amount of images.
	if len(sys.argv) > 1:
		try:
			images = int(sys.argv[1])
		except:
			print("Invalid input for amount of images:", sys.argv[1])
			return


	# Get images.
	start_time = time.time()
	for i in range(0, images):
		print("Getting image #", i+1)
		success = get_image()
		while not success:
			fails+=1
			print("FAILED - image was removed, trying again!")
			success = get_image()
		print()

	# Stop time.
	end_time = time.time() - start_time
	clean_time = time.strftime("%H:%M:%S", time.gmtime(end_time))

	print("Finished in", clean_time, "(H:M:S).")
	print("There were", fails, "unavailable images.")

# Run main code if we are the main module.
if __name__ == '__main__':
	main()
