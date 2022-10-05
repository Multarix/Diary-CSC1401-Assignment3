# All of our imports, these are built-in libraries
from __future__ import annotations  # Type hinting
from typing import TypedDict		# Type hinting
from datetime import datetime		# Only using this to get the current date and time
import json  						# This technically doesn't get used

# Appointment Dictionary type for expanded records
class Appointment(TypedDict, total=False):
	priority: str
	day: int
	month: int
	year: int
	start: int
	end: int
	description: str


# Bools that are lowercase are so much nicer
true = True
false = False



# Set up our diary class
class Diary:
	"""
	Methods:
		addRecord() -> None:
			Add new record(s) to the diary
		
		showRecords() -> None:
			Show all the records in the diary
		
		sortRecords() -> Bool:
			Sort the records by priority or time.
	"""
	# Init function for the diary class - Sets up everything we need
	def __init__(this, records: list[str] = []) -> None:
		"""
		Initialise the diary
		
		Args:
			records (list[Appointment], optional): A pre-existing record set. Defaults to [].
		"""
		# We support loading existing records if we have them, otherwise we init with an empty list
		if(len(records) > 0):
			print(f"Loading {len(records)} existing records...");
		
		this.records = records;
	
	
	
	
	# Expand records from string format
	def _expandRecords(cls) -> list[Appointment]:
		"""
		Expands the records into an a list of dictionary objects
		
		Returns:
			List[Appointment]: A list of Appointment dictionary's
		"""
		expanded: list[Appointment] = [];
		
		delimiter = ";";
		dateSplit = "/";
		for record in cls.records:
			# Split the string into an array of strings
			dataArray = record.split(delimiter);
			
			# Split the date so we access the day, month and year easier
			date = dataArray[1].split(dateSplit);
			
			# If the description has an ';' when it was originally inputted, our array will be longer than 5
			# So we need to add all the extra elements to the description joined with ';'
			# Because all other functions that deal with the description aside from the addRecord function use expandRecords(),
			# We only need to worry about checking the array length here, where our data is converted to the Appointment dictionary type
			description = dataArray[4];
			if(len(dataArray) > 5):
				for i in range(5, len(dataArray)):
					description += f";{dataArray[i]}";
			
			# Apply all the data to a Dictionary
			a: Appointment = {
				"priority": dataArray[0],
				"day": int(date[0]),
				"month": int(date[1]),
				"year": int(date[2]),
				"start": int(dataArray[2]),
				"end": int(dataArray[3]),
				"description": description
			};
			
			# Append the dict to a list
			expanded.append(a);
		
		return expanded;
	
	
	
	
	# Function to get the current time
	# To be used in the addRecord() function -> Using in the isValidDate function is against the assignment spec
	def _getCurrentTime(cls) -> dict:
		"""
		Returns the date and hour in a dictionary
		
		Returns:
			dict: The time in a dictionary format
		"""
		currDate = datetime.now().strftime("%d %m %Y %H");
		dateArray = currDate.split(" ");
		dateObject = { "day": int(dateArray[0]), "month": int(dateArray[1]), "year": int(dateArray[2]), "hour": int(dateArray[3]) };
		return dateObject;
	
	
	
	
	def _isFutureTime(cls, newRecord: dict) -> bool:
		"""
		Returns true or false depnding on if the time is in the future
		
		Returns:
			bool: True if the time is in the future, False if not
		"""
		
		# Get the current time
		currTime = cls._getCurrentTime();
		
		# Error messages here should be self explanatory for whats happening
		if(newRecord["year"] < currTime["year"]):
			print("Error: Year must be greater than or equal to the current year!");
			return false;
		
		# If the year is the same, we now check the month
		if(newRecord["year"] == currTime["year"]):
			
			if(newRecord["month"] < currTime["month"]):
				print("Error: Month must be greater than or equal to the current month!");
				return false;
			
			# If the month is the same, we now check the day
			if(newRecord["month"] == currTime["month"]):
				
				if(newRecord["day"] < currTime["day"]):
					print("Error: Day must be greater than or equal to the current day!");
					return false;
					
				# If the day is the same, we now check the hour
				if(newRecord["day"] == currTime["day"]):
					
					if(newRecord["hour"] is not None):
						if(newRecord["hour"] <= currTime["hour"]):
							print("Error: Hour must be greater than the current hour!");
							return false;
		
		# All checks passed, return true
		return true;
	
	
	
	
	# Function to check if a year is a leap year
	def _isLeapYear(cls, year: int) -> bool:
		"""
		Returns true or false depnding on if the year is a leap year
		
		Args:
			year (int): An integer number to check if it would be a leap year
		
		Returns:
			bool: True if the year is a leap year, False if not
		"""
		if(year % 100 == 0): # If the year is divisible by 100
			return true if(year % 400 == 0) else false; # If it is divisible by 400, it's a leap year

		return true if(year % 4 == 0) else false; # If it is divisible by 4, it's a leap year
	
	
	
	
	# Check if a date is valid
	def _isValidDate(cls, day: int, month: int, year: int) -> bool:
		"""
		Returns true or false depnding on if the date is valid

		Args:
			day (int): The day of the month
			month (int): The month of the year
			year (int): The year

		Returns:
			bool: True if the date is valid, False if not
		"""
		
		# If the year is less than 10000 and greater than or equal to 2022, it's a valid year
		if(10000 > year >= 2022): # This has the same effect as 10000 > year > 2021
			pass; # Cheeky
		else:
			print("Error: Year must be between 10000 and 2022");
			return false;
		
		# If the month is less than or equal to 12 and greater than or equal to 1, it's a valid month
		if(1 <= month <= 12):
			pass;
		else:
			print("Error: Month must be between 1 and 12");
			return false;
		
		# We now check if the year is supposed to be a leap year
		leapYear = cls._isLeapYear(year);
		
		# For february, we determine if it has 29 or 28 days depending on if it's a leap year
		febDays = 29 if(leapYear) else 28;
		
		# Dictionary for the days in each month
		daysInMonth = {
			1: { "name": "January", "days": 31 },
			2: { "name": "February", "days": febDays },
			3: { "name": "March", "days": 31 },
			4: { "name": "April", "days": 30 },
			5: { "name": "May", "days": 31 },
			6: { "name": "June", "days": 30 },
			7: { "name": "July", "days": 31 },
			8: { "name": "August", "days": 31 },
			9: { "name": "September", "days": 30 },
			10: { "name": "October", "days": 31 },
			11: { "name": "November", "days": 30 },
			12: { "name": "December", "days": 31 }
		};
		
		# Check if the day is less than or equal to the days in the month, but greater than 1
		if(1 <= day <= daysInMonth[month]["days"]):
			return true;
		else:
			print(f"Error: Day must be between 1 and {daysInMonth[month]['days']} for the month of {daysInMonth[month]['name']}!");
			return false;
	
	
	
	
	# Check if a time is valid
	def _isValidTime(cls, start: int, end: int) -> bool:
		"""
		Returns true or false depending on if the time is valid
		
		Args:
			start (int): The start time
			end (int): The end time
		
		Returns:
			bool: True if the time is valid, False if not
		"""
		# If the start time is greater than or equal to the end time, it's not valid
		if(start >= end):
			print("Error: Start time must be before end time!");
			return false;
		
		# If the start time and/ or end time is outside of the range 7-22, it's not valid
		if(7 <= start <= 22):
			pass; # Cheeky
		else:
			print("Error: Start time must be between 7 and 22!");
			return false;
			
		if(7 <= end <= 22):
			pass; # Cheeky
		else:
			print("Error: End time must be between 7 and 22!");
			return false;
		
		# Passed all checks, return true
		return true;
	
	
	
	
	# Check if a record overlaps with another record
	def _isConcurrentAppointment(cls, newApp: Appointment) -> bool:
		"""
		Checks if an appointment overlaps with another appointment
		
		Args:
			newApp (Appointment): The new appointment to check against existing records
		
		Returns:
			bool: True if there is an overlap, otherwise false
		"""
		# Expand the records into a more usable format
		records = cls._expandRecords();
		
		concurrent = false;
		for record in records:
			if(newApp["year"] == record["year"] and newApp["month"] == record["month"] and newApp["day"] == record["day"]):
				
				# If the start times are equal, return false
				if(newApp["start"] == record["start"]):
					return true
				
				# If existingRecordEnd > newRecordStart > existingRecordStart return true
				if(record["end"] > newApp["start"] > record["start"]):
					return true;
				
				# If newRecordEnd > existingRecordStart > newRecordStart return true
				if(newApp["end"] > record["start"] > newApp["start"]):
					return true;
		
		return false
	
	
	
	
	# Add records to the diary
	# Realistically should have split this into multiple smaller functions
	def addRecord(cls) -> None:
		"""
		Adds a record to the diary
		
		Asks the user for the following information:
			Date, Start Time, End Time, Description
		"""
		date = ""
		while(true):
			
			# Get the date and make sure it's valid or "end"
			while(true):
				while(true):
					date = input("\nEnter the date of the appointment (dd/mm/yyyy) type 'END' to exit: ");
					
					# Our break word
					if(date == 'END'):
						print('\nExiting function...');
						
						# Call showRecords() as we were instructed, and end the function
						return cls.showRecords();
					
					# Split the date using "/" as the delimiter
					dateint = date.split("/");
					
					# If dateint is 3, we break this loop
					if(len(dateint) == 3):
						break;
					
					# Otherwise, we print an error message and continue looping
					print("Error: Invalid date format!");
				
				# Check if the numbers can be converted to integers if so do it
				# Weird fake ternaries to make sure we don't get an error
				day = int(dateint[0]) if dateint[0].isdigit() else "bad";
				month = int(dateint[1]) if dateint[1].isdigit() else "bad";
				year = int(dateint[2]) if dateint[2].isdigit() else "bad";
				
				# Check if the day/month/year were correctly converted to numbers, if not restart loop
				if(day == "bad" or month == "bad" or year == "bad"):
					print("Error: Invalid date format!");
					continue;
				
				validDate = cls._isValidDate(day, month, year);
				
				# If the the date is invalid, restart the loop
				if(not validDate):
					continue;
				
				# Check if the appointment is in the future/ same day so far
				futureAppointment = cls._isFutureTime({ "day": day, "month": month, "year": year, "hour": None });
				if(futureAppointment):
					break;
			# The date is theoretically valid so far
			
			
			# Get the start and end times and make sure they're valid
			while(true):
				# Get the start time and make sure it's somewhat valid
				while(true):
					start = input("\nEnter the start time of the appointment (hh): ");
					startint = int(start) if start.isdigit() else "bad";
					
					# If startint isn't bad, we can break this loop
					if(startint != "bad"):
						break;
					
					print("Error: Invalid start time format!");
				
				
				# Get the end time and make sure it's somewhat valid
				while(true):
					end = input("\nEnter the end time of the appointment (hh): ");
					endint = int(end) if end.isdigit() else "bad";
					
					# If endint isn't bad, we can break this loop
					if(endint != "bad"):
						break;
					
					print("Error: Invalid end time format!");
				
				
				validTime = cls._isValidTime(startint, endint);
				# If the time is invalid, restart the loop
				if(not validTime):
					continue;
				
				
				futureAppointment = cls._isFutureTime({ "day": day, "month": month, "year": year, "hour": startint });
				# If future appointment is true, the time is valid!
				if(futureAppointment):
					break;
			# Start and end times are somewhat valid at this point
			
			
			# Format date as required for isConcurrentAppointment()
			apmnt: Appointment = { "day": day, "month": month, "year": year, "start": startint, "end": endint };
			concurrent = cls._isConcurrentAppointment(apmnt);
			
			# If concurrent is true, we need to ask for a new date/ start/ end, so we restart the loop
			# This also prevents users getting stuck in an infinite loop if they entered a date that cannot have any more appointments
			if(concurrent):
				print("\nError: Appointment overlaps with another appointment!");
				continue;
			
			
			# Get the description of the appointment
			while(true):
				description = input("\nEnter the description of the appointment (Max of 30 characters): ");
				
				# If the description is within the required length, we can break this loop
				if(30 >= len(description) >= 1):
					break;
				
				# If it's empty
				if(len(description) == 0):
					print("Error: Description cannot be empty!");
				
				# If it's too long
				if(len(description) > 30):
					print("Error: Description is too long!");

			
			# Get the priority of the appointment
			while(true):
				priority = input("\nEnter the priority of the appointment (High/Low): ");
				correctPriority = (priority.lower() == "high" or priority.lower() == "low");
				
				if(correctPriority):
					cls.records.append(f"{priority};{day}/{month}/{year};{start};{end};{description}");
					print("Successfully added the appointment to the records!");
					break;
				
				print("Error: Invalid priority!");
	
	
	
	
	# Show all records in the diary
	def showRecords(this) -> None:
		"""
		Show all records in the diary
		
		Creates a table of all the records in the diary before printing it
		"""
		if(len(this.records) == 0):
			return print("Error: There are no records currently in the diary!");
			
		outputArray = [];
		delimiter = "\n";
		
		descLength: int = 7
		records = this._expandRecords();
		# For each record, we're going to give them a variable so we better understand and access the data
		for record in records:
			priority = record["priority"];
			day = record["day"];
			month = record["month"];
			year = record["year"];
			start = record["start"];
			end = record["end"];
			description = record["description"];
			
			# Make sure the the prioity, date, start and end will always be the same lengths
			priority = "Low " if(priority.lower() == "low") else "High";
			
			# 9 -> 09 etc
			# We do this to kinda cheat the system, we stored them correctly without the 0's in front
			# But then to display them and make our life easier, we make sure they're all the same length
			if(10 > day):
				day = f"0{day}";
			
			if(10 > month):
				month = f"0{month}";
			
			if(10 > start):
				start = f"{start} ";
			
			if(10 > end):
				end = f"{end} ";
			
			# Turn the date into the correct format
			date = f"{day}/{month}/{year}"
			
			# Make sure the description seperator matches the length of the title or longest description
			descLength = max(descLength, len(description))
			
			# Add to an output, adding in the predefined spaces.
			outputArray.append(f"{priority}        {date}     {start}        {end}      {description}");
		
		# Titles will always be in the same location
		headers = "\nPrioity     Date           Start     End     Subject\n";
		# Seperators will always be in the same location, but desc length may change length
		seperators = f"--------    ----------     -----     ---     {'-' * descLength}\n";
		
		output = headers + seperators + delimiter.join(outputArray);
		print(output);
	
	
	
	
	# Sort by Prioity Or Time
	def sortRecords(cls) -> bool:
		"""
		Sort records by either priority or time
		
		Returns:
			bool: False if the diary was not sorted, True if it was
		"""
		
		
		# Bubble sort algorithm
		def sort(array: list) -> list: # Worst case sort time is: O(n^2)
			"""
			Returns a sorted list using an implimentation of the bubble sort algorithm.
			We decided that due to the expected size of the diary, the bubble sort algorithm is good enough.
			
			Internal Function because it is only used in the sortRecords function
			
			Args:
				array (list): A list of integers to sort
			
			Returns:
				list: A sorted list
			"""
			
			for element in array:
				# Sorted starts at true and turns to false if an item was swapped during an iteration in the inside loop
				sorted = true;
				
				# LastSort starts at 1 because otherwise we'd try and compare the last element to 'nothing' on the first pass
				lastSort = 1;
				
				for i in range(len(array) - lastSort):
					# We grab 2 elements to compare
					itemA = array[i];
					itemB = array[i + 1];
				
					if(itemA <= itemB): # If the elements are in the "correct" order
						continue; # We go to the iteration
					
					# If the elements are in the wrong order, we swap them
					array[i] = itemB;
					array[i + 1] = itemA;
				
					# If we get to here, a change has been made
					if(sorted):
						sorted = false;
				
				if(sorted): # If no changes were made, we know that the array has been sorted
					break; # This Reduces time wasted in cases where the array might already be sorted or was close to sorted etc
				
				# The last check on the inner loop always puts an element in the correct spot, so we don't need to check it again
				# This also decreases our average sort time, sadly we can't do much more for this algorithm to improve its average sort time
				lastSort += 1;
			
			return array;
		
		
		# Progress bar
		def progressBar(progress: float) -> str:
			"""
			Returns a progress bar with a carriage return at the front
			Was added for fun, if there are several thousand records, you can see
			the sorting progress instead of thinking the program is stuck
			
			Internal function because it is only used in the sortRecords function
			
			Args:
				progress (float): A number between 0 and 1 to represent the progress
			"""
			bar = "\r[##             ]"
			if(progress >= 0.99):
				return "\r[############...]"  # 99%
			
			if(progress >= 0.9):
				return "\r[###########....]"  # 90%
			
			if(progress >= 0.8):
				return "\r[##########.....]"  # 80%
			
			if(progress >= 0.7):
				return "\r[#########......]"  # 70%
			
			if(progress >= 0.6):
				return "\r[########.......]"  # 60%
			
			if(progress >= 0.5):
				return "\r[#######........]"  # 50%
			
			if(progress >= 0.4):
				return "\r[######.........]"  # 40%
			
			if(progress >= 0.3):
				return "\r[#####..........]"  # 30%
			
			if(progress >= 0.2):
				return "\r[####...........]"  # 20%
			
			if(progress >= 0.1):
				return "\r[###............]"  # 10%
			
			return bar
		
		
		# Ask how to sort the records until the user enters a valid input or "end" - case insensitive
		# Valid inputs are "time" and "priority"
		
		sortMethod = false;
		
		while(true):
			print("\nHow would you like to sort the records?");
			print("Type 'PRIORITY' to sort by priority,");
			print("Type 'TIME' to sort by time,");
			print("Type 'END' to return to the main menu");
			choice = input("Enter your choice: ");
			choice = choice.lower();
			
			if(choice == "priority"):
				sortMethod = "priority";
				break;
			
			if(choice == "time"):
				sortMethod = "time";
				break;
			
			if(choice == "end"):
				print("\nExiting function...");
				return;
			
			else:
				print("Invalid input, please try again");
			
		
		
		# Regardless of the choice, I felt it was better to also sort the records by time
		# Also I spent all this time programming it, I at least want it used.
		
		# Things are going to get slightly complicated
		# We are going to make an object/ dict that will use key-pair-values to store the data
		# This will allow us to sort the data by sorting the keys.
		# The appointments will be stored in a format like so:
		#
		#	{
		#		Year: {
		#			Month: {
		#				Day: {
		#					Start time: {
		#						...Appointment
		#					}
		#				}
		#			}
		#		}
		#	}
		#
		# From there, we will sort the keys of each level into ascending order, which at the end will result in the data being sorted
		# We don't actually have to do this to sort the data, we could instead convert each appointment to the time since the epoch.
		# It would be a much cleaner method to sort, but this shows the understanding of how to manipulate data similar to this.
		
		
		
		print("\r[...............]", end="");  # Progress bar
		
		# Expand the records into a more usable format
		data = cls._expandRecords();
		appointments = {};
		
		print("\r[#..............]", end="");  # Progress bar
		
		for apmnt in data:
			# If the year is not in the dictionary, add it
			if(apmnt["year"] not in appointments):
				appointments[apmnt["year"]] = {};
			
			# If the month of the specified year is not in the dictionary, add it
			if(apmnt["month"] not in appointments[apmnt["year"]]):
				appointments[apmnt["year"]][apmnt["month"]] = {};
			
			# If the day of the specified month is not in the dictionary, add it
			if(apmnt["day"] not in appointments[apmnt["year"]][apmnt["month"]]):
				appointments[apmnt["year"]][apmnt["month"]][apmnt["day"]] = {};
			
			# Add the data to the dictionary setting the start-time as the key
			appointments[apmnt["year"]][apmnt["month"]][apmnt["day"]][apmnt["start"]] = apmnt;
		
		print("\r[##.............]", end="");  # Progress bar
		
		dataLength = len(data);
		totalSorted = 0;
		
		sortedArray = [];
		# sort the years into ascending order and iterate through them
		for year in sort(list(appointments.keys())):
			
			# sort the months into ascending order and iterate through them
			for month in sort(list(appointments[year].keys())):
				
				# sort the days into ascending order and iterate through them
				for day in sort(list(appointments[year][month].keys())):
					
					# sort the appointments into ascending order and iterate through them
					for start in sort(list(appointments[year][month][day].keys())):
						
						# Add the appointment to sortedArray. This should now have the dates sorted correctly via time
						sortedArray.append(appointments[year][month][day][start]);
						totalSorted += 1;
						print(progressBar(totalSorted / dataLength), end=""); # Progress bar
		
		# sortedArray is now sorted by time. I call this method "jank time sort".
		
		print("\r[#############..]", end="");  # Progress bar
		
		# Now we can sort via priority if that was required
		if(sortMethod == "priority"):
			high = [];
			low = [];
			
			for a in sortedArray:
				if(a["priority"] == "high"):
					# High prioity appointments will go into the high list
					high.append(a);
				else:
					# Low prioity appointments will go into the low list
					low.append(a);
			
			# We clear out the old sortedArray
			sortedArray.clear();
			high.extend(low); # Add the low priority appointments to the high list
			sortedArray.extend(high); # Add all the appointments to the sortedArray
		
		# Now we change the format back into a string for use with other functions
		rec = [];
		for appt in sortedArray:
			rec.append(f"{appt['priority']};{appt['day']}/{appt['month']}/{appt['year']};{appt['start']};{appt['end']};{appt['description']}");
		print("\r[##############.]", end=""); # Progress bar
		
		# And apply the data back to the records in the new order
		cls.records.clear();
		cls.records.extend(rec);
		print("\r[###############]", end=""); # Progress bar
		print(" Done!");
		
		return true



# Main function, will only be run if the file is not imported
def main() -> bool:
	saveRecords = false; # False by default, change to true if you want to save the records to a file
	
	diary = Diary();
	while(true):
		print("\nWhat would you like to do?");
		print("Type 'ADD' to add appointments,");
		print("Type 'SHOW' to show all appointments,");
		print("Type 'SORT' to sort all appointments,");
		print("Type 'END' to exit the program.");
		choice = input("Enter your choice: ");
		choice = choice.lower();
		
		if(choice == "add"):
			diary.addRecord();
			continue;
		
		if(choice == "show"):
			diary.showRecords();
			continue;
		
		if(choice == "sort"):
			diary.sortRecords();
			continue;
		
		if(choice == "end"):
			print("\nExiting program...");
			break;
		
		print("\nInvalid choice");
	
	if(saveRecords): # We added the ability to save the records to a file, saveRecords is false by default however
		json.dump(diary.records, open("records.json", "w"), indent="\t");
		return true;
	
	return false;