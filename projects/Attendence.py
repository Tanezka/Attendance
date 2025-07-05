import tkinter as tk
from datetime import datetime
import csv
import os
from PIL import Image, ImageEnhance, ImageFilter
from tkinter import filedialog
import pytesseract

CSV_FILE = "player_log.csv"

class myWindow:
	def __init__(self):
		# Window Setup
		self.window = tk.Tk()
		self.window.geometry("600x400")
		self.window.title("Attendance")

		# Variables
		self.pairs = []
		# Frame Setup
		self.frame1 = tk.Frame(self.window, bg="lightblue")	
		self.frame1.pack(side="left", fill="y", expand=False)
		self.col2 = tk.Frame(self.window, bg="purple")
		self.col2.pack(side="left", fill="both", expand=True)

		# Label Setup
		input_label = tk.Label(self.frame1, text="Yoklamayı yapıştırın:")
		input_label.grid(row=0, column=0, padx=10, pady=10)
		input_label_utc = tk.Label(self.frame1, text="Etkinliğin Tarihini girin (örn: 02/24/2025 18:45):")
		input_label_utc.grid(row=2, column=0, padx=10, pady=10)
		result_label = tk.Label(self.col2, text="Yoklama Sonucu:")
		result_label.grid(row=0, column=0, padx=10, pady=10)
		white_flag_label = tk.Label(self.frame1, text="Content'e katılan oyuncular:")
		white_flag_label.grid(row=4, column=0, padx=10, pady=10)

		# Input Setup
		input_box = tk.Text(self.frame1, width=30, height=2)
		input_box.grid(row=1, column=0, padx=10)
		input_utc_box = tk.Entry(self.frame1, width=30)
		input_utc_box.grid(row=3, column=0, padx=10)
		input_white_flag_box = tk.Text(self.frame1, width=30, height=2)
		input_white_flag_box.grid(row=5, column=0, padx=10)

		# Button
		button = tk.Button(self.frame1, text="Yoklama al", command=lambda: calculateAttendance(input_box.get("1.0", "end"), input_utc_box.get(), input_white_flag_box.get("1.0", "end"), self.pairs))
		button.grid(row=6, column=0, padx=10, pady=10)
		log_button = tk.Button(self.frame1, text="Yoklamayı Kaydet", command=lambda: update_attendance_log(self.pairs, self))
		log_button.grid(row=7, column=0, padx=10, pady=10)
		# Button Setup
		# self.button = tk.Button(self.frame1, text="Troll But", command=lambda: self.makeNewWindow())
		# self.button.grid(row=5, column=0, sticky = "n")

		# Button Image
		# self.button_img = tk.Button(self.frame1, text="Open image", command=lambda: open_file_dialog())
		# self.button_img.grid(row=6, column=0)

		# Result Text
		self.result_text = tk.Text(self.col2, height=10, width=25)
		self.result_text.grid(row=1, column=0, padx=10, pady=10)

	def	makeNewWindow(mainWindow):
		tempWindow = newWindow()
		tempWindow.countDown(mainWindow, 3)

def calculateAttendance(list, time, white_flag_list, pairs):
	if list.strip() == "" or time.strip() == "" or white_flag_list.strip() == "":
		print("Input is empty")
		return
	pairs.clear()
	TestWindow.result_text.delete("1.0", tk.END)
	dt2 = datetime.strptime(time, '%m/%d/%Y %H:%M')
	forscience = list.split('\n')
	forscience = forscience[1:]
	contenders = white_flag_list.lower().replace(' ', '').replace('0', 'o').split()
	for line in forscience:
		if line.strip() == "":
			continue
		parts = line.replace('"', '').split('\t')
		if (parts[1] == "Online"):
			if parts[0].lower().replace('0', 'o') not in contenders:
				pairs.append((parts[0], "Online"))
			continue
		dt1 = datetime.strptime(parts[1][:-3], '%m/%d/%Y %H:%M')
		diff = dt2 - dt1
		diff_minutes = int(diff.total_seconds() / 60)
		if diff_minutes < 60 and diff_minutes > 0:
			pairs.append([parts[0], int(diff_minutes)])
	
	for element in pairs:
		# print(f"{element[0]} is dodging with {element[1]} mins\n")
		TestWindow.result_text.insert(tk.END, f"{element[0]} - {element[1]}\n")


def open_file_dialog():
	filepath = filedialog.askopenfilename(
		title="Select an image",
		filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
	)
	if filepath:
		print("Selected file:", filepath)
		img = Image.open(filepath)
		img = img.convert('L')  # convert to grayscale
		img = img.filter(ImageFilter.SHARPEN)  # sharpen the image
		img.show()
		test1 = pytesseract.image_to_string(img)
		print("Extracted text:", test1)

def update_attendance_log(pairs, mainWindow):
	if not pairs:
		return
	print("Updating attendance log...")
	for player, status in pairs:
		print(f"Player: {player}, Status: {status}")
		update_player_log(player, status)
	
	# makeNewWindow = myWindow.makeNewWindow(mainWindow)


def load_player_log():
	player_log = {}
	if os.path.exists(CSV_FILE):
		with open(CSV_FILE, mode='r', newline="", encoding="utf-8") as file:
			reader = csv.DictReader(file)
			for row in reader:
				player_log[row["player_name"]] = {
					"dodge_count": int(row["dodge_count"]),
					"skip_count": int(row["skip_count"]),
					"avarage_dodge_time": int(row["avarage_dodge_time"])
				}
	return player_log

def save_player_log(player_log):
	with open(CSV_FILE, mode='w', newline="", encoding="utf-8") as file:
		fnames = ["player_name", "dodge_count", "skip_count", "avarage_dodge_time"]
		writer = csv.DictWriter(file, fieldnames = fnames)
		writer.writeheader()
		for player_name, data in player_log.items():
			writer.writerow({
				"player_name": player_name,
				"dodge_count": data["dodge_count"],
				"skip_count": data["skip_count"],
				"avarage_dodge_time": data["avarage_dodge_time"]
			})

def update_player_log(player_name, status):
	log = load_player_log()

	if player_name not in log:
		log[player_name] = {
			"dodge_count": 0,
			"skip_count": 0,
			"avarage_dodge_time": 0
		}
	if status == "Online":
		log[player_name]["skip_count"] += 1
	
	else:
		log[player_name]["dodge_count"] += 1
		log[player_name]["avarage_dodge_time"] = int((log[player_name]["avarage_dodge_time"] * log[player_name]["dodge_count"] + int(status)) / (log[player_name]["dodge_count"]))
	
	save_player_log(log)

class newWindow:
	def	__init__(self):
		self.window = tk.Toplevel()
		self.window.geometry("300x100")
		self.text = tk.StringVar()
		self.text.set("Kayıt başarı ile tutuldu. Pencere 3 saniye içinde kapanacaktır.")	
		self.myLabel = tk.Label(self.window, textvariable=self.text)
		self.myLabel.pack()
		self.window.title("TestWindow")
		# self.exitButton = tk.Button(self.window, text="Close", command=lambda: self.countDown(3))
		# self.exitButton.pack()

	def countDown(self, window, count):
		if count > 0:
			self.myLabel.after(1000, self.countDown, window, count - 1)
		else:
			self.window.destroy()
			window.window.destroy()


TestWindow = myWindow()
TestWindow.window.mainloop()