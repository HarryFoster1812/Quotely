###################### Imports ######################

from tkinter import *  
from tkinter import scrolledtext
from functools import partial
import json
import time
import pickle
import webbrowser
import math
import os

try:
    import urllib3
    from PIL import Image, ImageTk
    from bs4 import BeautifulSoup
    import lxml

except: # if one of the modules are not installed

    os.system('pip3 install -r Misc\\requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org') # trys to install the modules

    import urllib3
    from PIL import Image, ImageTk
    from bs4 import BeautifulSoup
    import lxml

###################### Global Variables ######################

quotes = []
requested_quotes = []
i = 1
current = ''
next = ''
http = urllib3.PoolManager()

###################### OOP ######################

class quote:

    def __init__(self, info): # constructor

        self.quote = info[0]
        self.author = info[1]
    
    def Get_info(self): # Method to return the values of the quote object
        return (self.quote, self.author)
    
    def Get_info_lower(self):
        return (self.quote.lower(), self.author.lower())

    def Get_quote_lower(self):
        return self.quote.lower()

class Application:

    def __init__(self, root): # constructor

        self.Offline_mode=IntVar(value=1) # creates a tk variable

        self.button_frame = Frame(root) # create a frame for the buttons to go in
        self.button_frame.place(x=0, y=0, relheight=1.0, relwidth=0.172) # place it in the root (the window) at x=0 and y=0

        self.Home = Button(self.button_frame, text='Home', font = ('Segoe UI', 20), bg = 'white', fg = 'black', command = lambda: (self.home_page())) # create the home button
        self.Home.place(x=0, y=0, relheight=0.142857142857, relwidth=1) # see working

        self.New = Button(self.button_frame, text='New', font = ('Segoe UI', 20), bg = 'white', fg = 'black', command = lambda: (self.new_page())) # create the new button
        self.New.place(x=0, rely=0.142857142857, relheight=0.142857142857, relwidth=1)

        self.View = Button(self.button_frame, text='View', font = ('Segoe UI', 20), bg = 'white', fg = 'black', command = lambda: (self.view_page())) # create the view button
        self.View.place(x=0, rely=(0.142857142857*2), relheight=0.142857142857, relwidth=1)

        self.Search = Button(self.button_frame, text='Search', font = ('Segoe UI', 20), bg = 'white', fg = 'black', command = lambda: (self.search_page())) # create the search button
        self.Search.place(x=0, rely=(0.142857142857*3), relheight=0.142857142857, relwidth=1)

        self.Add = Button(self.button_frame, text='Add', font = ('Segoe UI', 20), bg = 'white', fg = 'black', command = lambda: (self.add_page())) # create the add button
        self.Add.place(x=0, rely=(0.142857142857*4), relheight=0.142857142857, relwidth=1)

        self.Remove = Button(self.button_frame, text='Remove', font = ('Segoe UI', 20), bg = 'white', fg = 'black', command = lambda: (self.remove_page())) # create the edit button
        self.Remove.place(x=0, rely=(0.142857142857*5), relheight=0.142857142857, relwidth=1)

        self.Author = Button(self.button_frame, text='About', font = ('Segoe UI', 20), bg = 'white', fg = 'black', command = lambda: (self.author_page())) # create the remove button
        self.Author.place(x=0, rely=(0.142857142857*6), relheight=0.142857142857, relwidth=1)

        self.content_frame = Frame(root)
        on_startup()
        self.home_page()
    
    def home_page(self):

        self.dimensions_update()
        self.content_frame.destroy() # destroys the previous page
        self.content_frame = Frame(root) # creates it again, basicly it like clears the page
        self.content_frame.place(relx=0.172, y=0) # places it
        self.reset_buttons() # sets all the buttons back to white
        self.Home.config(bg = '#008CBA', fg = 'white') # change the button to blue

        self.picture('Data\\Images\\home_background.png')
        self.canvas.create_text(((self.window_width*0.414)), self.window_height/2, text = "Make Good Choices\n    - Maya Vaghela", font=('Segoe UI', 40), fill='white') # places the text
    
    def new_page(self): # im not going to comment in ths because most of it is repeated code (kinda)

        self.dimensions_update()
        self.content_frame.destroy()
        self.content_frame = Frame(root)
        self.content_frame.place(relx=0.172, y=0, relheight=1, relwidth=0.828)
        self.reset_buttons()
        self.New.config(bg = '#008CBA', fg = 'white')
        
        self.picture('Data\\Images\\Quote_background.png')

        self.current_quote = self.canvas.create_text(((self.window_width*0.828)/2), 160, text=('"'+current[0]+'"\n\n'+'- '+current[1]), font=('Segoe UI', 20), width=500, fill='black') # displays the current

        if current[1] == '':
            Button(self.content_frame, text='Retry', bg='black', fg='white', command=lambda:(on_startup(), self.new_page())).place(rely=(0.142857142857*5-0.142857142857/2/2), relx=(0.5-0.2077294686/2), relheight=(0.142857142857/2), relwidth=(0.2077294686)) # creates a retry button
    
        else:
            Button(self.content_frame, text='Yes', bg='black', fg='white', command=lambda: self.on_next(True)).place(rely=(0.142857142857*5-0.142857142857/2/2), relx=(0.1980676329-0.2077294686/2), relheight=(0.142857142857/2), relwidth=0.2077294686) #yes button
            Button(self.content_frame, text='No', bg='black', fg='white', command=lambda: self.on_next()).place(rely=(0.142857142857*5-0.142857142857/2/2), relx=((0.80193236715-(0.2077294686/2))), relheight=(0.142857142857/2), relwidth=0.2077294686) # no button

    def view_page(self):

        self.dimensions_update()
        self.content_frame.destroy()
        self.content_frame = Frame(root)
        self.content_frame.place(relx=0.172, y=0, relheight=1, relwidth=0.828)
        self.reset_buttons()
        self.View.config(bg = '#008CBA', fg = 'white')

        self.text = scrolledtext.ScrolledText(self.content_frame, state="normal") # creates a scolled text widget
        self.populate(0) # calls the populate method
        self.text.configure(state='disabled') # disable it so the user can't edit them
        self.text.place(relheight=(0.142857142857*6), relwidth=1) # places the scolled text

        self.page_button_frame = Frame(self.content_frame)
        self.page_button_frame.place(rely=0.918571428)
        self.amount_of_page_buttons = math.ceil((len(quotes)/25)) # math.ceil rounds the value to the highest so 4.1 would round to 5 we do this beacause we can't have a "fraction of a button" in a sense (idk why im explaining this you probably understand already, well I wrote it and i'm not deleting it so yeah)
        self.page_button_populate(0) # calls the button populate method

    def search_page(self):

        self.dimensions_update()
        self.content_frame.destroy()
        self.content_frame = Frame(root)
        self.content_frame.place(relx=0.172, y=0, relheight=1, relwidth=0.828)
        self.reset_buttons()
        self.Search.config(bg = '#008CBA', fg = 'white')

        self.dropdown = Button(self.content_frame, text='☰', bg='white', command = self.search_menu) # creates button
        self.dropdown.place(relx = 0.144927536232, rely = 0.0493333333333, relheight=0.0466666666666) # maths.
        
        self.search_query = Entry(self.content_frame, font=('Segoe UI', 12)) # the entry field
        self.search_query.place(relx=0.194847020934, rely=0.044, relheight=0.0466666666666, relwidth=0.5958132045088) # more maths.
        
        self.search_button = Button(self.content_frame, text='🔍', bg='white', command = lambda: self.display_results(search(self.search_query.get(), self.Offline_mode.get()))) # creates the search button
        self.search_button.place(relx = 0.800322061192, rely = 0.0493333333333, relheight=0.0466666666666) # even more maths.
        
        self.amount_of_results = Label(self.content_frame, text='0 results found', font=('Segoe UI', 15)) # the amount of results
        self.amount_of_results.place(rely=0.226666667, relx=0.39452496) # you guessed it, maths.

        self.scroll_results = scrolledtext.ScrolledText(self.content_frame, wrap=WORD) # creates the scrolled text that shows the results
        self.scroll_results.configure(state='disable') # disables it
        self.scroll_results.place(rely=0.288, relx=0.122383253, relheight=0.569333333, relwidth=0.755233494)

    def add_page(self):

        self.dimensions_update()
        self.content_frame.destroy()
        self.content_frame = Frame(root)
        self.content_frame.place(relx=0.172, y=0, relheight=1, relwidth=0.828)
        self.reset_buttons()
        self.Add.config(bg = '#008CBA', fg = 'white')

        self.picture('Data\\Images\\Add_background.png')

        self.container = Frame(self.content_frame, bg='black') # creates a frame for the entry to be placed in
        self.container.place(relx=0.45,rely=0.128,relwidth=0.45,relheight=0.45)
        
        Label(self.container, text='Quote', bg='black', fg='white').place(relx=0.1,rely=0.2)
        self.quote_entry = Entry(self.container) # user entry
        self.quote_entry.place(relx=0.3,rely=0.2, relwidth=0.58, relheight=0.08)

        Label(self.container, text='Author', bg='black', fg='white').place(relx=0.1,rely=0.45)
        self.author_entry = Entry(self.container) # author entry
        self.author_entry.place(relx=0.3,rely=0.45, relwidth=0.58, relheight=0.08)

        Button(self.container, text='Add!', command = lambda:(Add((self.quote_entry.get(), self.author_entry.get())), self.quote_entry.delete(0, 'end'), self.author_entry.delete(0, 'end'))).place(relx=0.43,rely=0.79, relwidth=0.18,relheight=0.08) # add button

    def remove_page(self):

        self.dimensions_update()
        self.content_frame.destroy()
        self.content_frame = Frame(root)
        self.content_frame.place(relx=0.172, y=0, relheight=1, relwidth=0.828)
        self.reset_buttons()
        self.Remove.config(bg = '#008CBA', fg = 'white')
        
        self.picture('Data\\Images\\Remove_background.png')

        self.container = Frame(self.content_frame, bg='black')
        self.container.place(relx=0.05, rely=0.4, relwidth=0.3, relheight=0.18)

        Label(self.container, text='Quote', bg='black', fg='white').place(relx=0.1,rely=0.4)
        self.quote_entry = Entry(self.container)
        self.quote_entry.place(relx=0.35,rely=0.4, relwidth=0.45, relheight=0.1)
        Button(self.container, text='Remove', command = lambda:(remove(self.quote_entry.get()), self.quote_entry.delete(0, 'end'))).place(relx=0.35,rely=0.69) # delete button
    
    def author_page(self):

        self.dimensions_update()
        self.content_frame.destroy()
        self.content_frame = Frame(root)
        self.content_frame.place(relx=0.172, y=0, relheight=1, relwidth=0.828)
        self.reset_buttons()
        self.Author.config(bg = '#008CBA', fg = 'white')

        self.picture('Data\\Images\\Author_background.png')
        self.clickme = Label(self.canvas, text='Click me', font=('Segoe UI', 20)) # click me label
        self.clickme.place(relx=0.45, rely=0.5)
        self.clickme.bind("<Button-1>", lambda e: webbrowser.open_new('https://Click-me.harryfoster1812.repl.co')) # open the website...

    def reset_buttons(self, *args): # Used to set all the buttons back to white

        self.Home.config(bg = 'white', fg = 'black')
        self.New.config(bg = 'white', fg = 'black')
        self.View.config(bg = 'white', fg = 'black')
        self.Search.config(bg = 'white', fg = 'black')
        self.Add.config(bg = 'white', fg = 'black')
        self.Remove.config(bg = 'white', fg = 'black')
        self.Author.config(bg = 'white', fg = 'black')
    
    def dimensions_update(self):

        self.window_width = root.winfo_width() # use some common sense.
        self.window_height = root.winfo_height() # this time use some logic as well.

    def picture(self, image_location):

        self.canvas = Canvas(self.content_frame, width = (self.window_width*0.828), height = self.window_height) # creates canvas
        self.canvas.pack() # packs it

        self.image = Image.open(image_location).resize((round(self.window_width*0.828), round(self.window_height))) # opens the image and resises it based on the window
        self.image = ImageTk.PhotoImage(self.image) # makes it a tkinter photo

        self.canvas.create_image(0, 0, image = self.image, anchor='nw') # draws the image to the canvas

    def on_next(self, accept=False): # when the user pushes the "yes" or "no" button, the line accept=False sets the default value of the parameter to false
        global current, next, i

        if accept: # if the user clicked yes
            Add(current) # calls the add function

        current = next # the current quote becomes the next one
        i += 1 # increments i by 1 each time one of the buttons is pressed

        if i >= 50:
            get_quotes() # refreshes the quote list 
            i=0 # sets i to 0

        next = (requested_quotes[i][0], requested_quotes[i][1]) # sets the next quote
        self.canvas.itemconfig(self.current_quote, text=('"'+current[0]+'"\n\n'+'- '+current[1])) # Changes the quote that the user sees to the new quote

    def populate(self, page):

        self.text.configure(state='normal') # set the state to normal so we can edit the content
        self.text.delete('1.0', END) # clear the widget

        for j in range(25 if (len(quotes)-(25*page)) > 25 else (len(quotes)-(25*page))): # i honestly though this would throw a snytax error, but hey it works.
            info = quotes[(25*page)+j].Get_info() # get the index
            self.text.insert('end', ('\n"'+info[0]+'"\n\n'+'- '+info[1]+'\n')) # display the quote
            self.text.insert('end',( '_'*round((self.window_width*0.828)/8.28))+'\n') # disply the divider to make them look nicer

    def page_button_populate(self, page): # this enitre method i am so proud of like i just feel like it is one of the best things i have done
        self.page_button_frame.destroy()
        self.page_button_frame = Frame(self.content_frame)

        if page > 0:
            Button(self.page_button_frame, text="<-", command=partial(self.page_button_populate, (page-1))).pack(side='left') # create the back button
            
        self.page_no = 5*page # set the current starting page number to be a multiple of 5

        for j in range(5 if (self.amount_of_page_buttons)-(5*page) > 5 else (self.amount_of_page_buttons-(5*page))): # the same things as the for lopp in the populate method
            Button(self.page_button_frame, text=((5*page)+j+1), command=partial(self.populate, self.page_no)).pack(side='left') # Creates the page buttons
            self.page_no += 1 # increments the page number by one 
        
        if (self.amount_of_page_buttons)-(5*page) > 5: # if there are more pages to be displayed add a forwards button
            Button(self.page_button_frame, text="->", command=partial(self.page_button_populate, (page+1))).pack(side='left')
            
        self.page_button_frame.place(rely=0.918571428, relx=0.35) # no idea of how to do the relx so i just put 0.35 because why not?

    def search_menu(self, option=True):
        if option: # when the user presses the ☰ button

            self.dropdown.config(text='╳', command = partial(self.search_menu, False))
            self.search_menu_frame = Frame(self.content_frame, bg='white')
            self.search_menu_frame.place(relx=0.144927536232, rely=0.108)
            Label(self.search_menu_frame, text='Options', bg='white').pack()
            self.offline_checkbox = Checkbutton(self.search_menu_frame, text='Offline mode', variable=self.Offline_mode, bg='white').pack()

        else: # when the user pesses the ╳ button

            self.dropdown.config(text='☰', command = self.search_menu) # reconfigures the button
            self.search_menu_frame.destroy() # deletes the dropdown menu
    
    def display_results(self, results):

        self.scroll_results.configure(state='normal')
        self.scroll_results.delete('1.0', END) 

        if len(results) == 0:
            self.scroll_results.insert('end', ('Sorry, we could not find what you were looking for, check your spelling and try again')) # lol it found nothing

        for j in results:
            self.scroll_results.insert('end', ('\n"'+j[0]+'"\n\n'+'- '+j[1]+'\n')) # display the quote
            self.scroll_results.insert('end',( '_'*round((self.window_width*0.828)/11.0892857))+'\n')
        
        self.scroll_results.configure(state='disable') # disables the scrollable text
        self.amount_of_results.config(text=f'{len(results)} results found') # changes the label to say the amount of results that were found

###################### Functional Programming ######################

def Add(Info): # idk why i made this i just did, i know it is like less efficent but like who cares

    if Info[0] == '': # if the user typed nothing
        return 
    quotes.append(quote(Info)) # Creates a quote object and appends it to the list of quotes

def on_startup():
    global current, next
    try:
        get_quotes() # Requests list of 50 quotes
        current = requested_quotes[0] # sets the first item in the array to current
        next = requested_quotes[1]

    except Exception: # if the users has no wifi
        current = ["Couldn't connect to the internet, please check you connection and try again.", ""] # Shows offile error message

def remove(quote):
    quote = quote.lower() # puts it into lower form
    for j in enumerate(quotes): # when using the enumerate function the value of j would be (0 (the index, this increments by one each itteration), __object__)
        if quote == j[1].Get_quote_lower():
            quotes.pop(j[0]) # removes using the index

def get_quotes():
    r = http.request('GET', 'https://zenquotes.io/api/quotes') # Sends a request to the api
    r = json.loads(r.data.decode("utf-8"))
    requested_quotes.clear() #  Clears the existing array so it is empty
    for j in range(50): # 50 is used because that is the amount of quotes the api sends
        Requested_Quote = r[j]["q"]
        if '�' in Requested_Quote: #often the api won't reconise the ' charcter and replace it with the � character
            Requested_Quote = Requested_Quote.replace("�", "'") # Replaces the � with '
        requested_quotes.append([Requested_Quote, r[j]['a']]) # Appends the information
    

def read_write(mode):
    global quotes
    if mode == 'read':
        with open('Data\\quotes.dictionary', 'rb') as quotes_file: # uses the pickle module to read the objects from file
            quotes = pickle.load(quotes_file) # loads the contents of the file to the quotes array

    else:
        with open('Data\\quotes.dictionary', 'wb') as quotes_file: # uses the pickle module again
            pickle.dump(quotes, quotes_file) # Writes the array to a file, uses the pickle module because it writes objects to files

def search(query, mode):
    query = query.lower() # makes ot lower case
    results = [] # declare the results list
    if mode: # if offline mode is True
        for j in quotes: # Tbh, i cbb (can't be bothered (I can't swear/say a "bad word")) to explain but imma do it anyway
            info = j.Get_info_lower() # calls the lower method so we get the quote and the author in lowercase form
            if query in info[0]:
                results.append(j.Get_info())
            elif query in info[1]:
                results.append(j.Get_info())

    else: # if offline mode is False
        try: # just incase an error occurs 😢
            query = query.replace(' ', '+') # Turn the user input to somthing that can acctually be searched
            source = http.request('GET', f"https://www.brainyquote.com/search_results?x=0&y=0&q={query}") # Sends a request
            soup = BeautifulSoup(source.data, 'lxml') # Turns the request into soup
            quotelist = soup.find(id='quotesList') # finds the element that contains all the quotes
            quotes_ = quotelist.find_all(title = 'view quote') # finds the quotes from the element 
            authors = quotelist.find_all(title = 'view author') # finds the authors from the element 

            for j in enumerate(quotes_): # sometimes there are images, we take care of that by removing them
                if '\n' in j[1].text: # finds the image
                    quotes_.pop(j[0]) # removes it

            for l, j in zip(quotes_, authors): # zip is used so we can pass two variables at the same time into to the loop
                results.append((l.text, j.text)) # appends it to a format that we use

        except Exception as e: # say the user did not have any wifi, they could not request anything, so we would get an error
            return [] # Returns an empty list

    return results

###################### Main ######################

if __name__ == '__main__': # so I can import other functions without them running

    read_write('read') # Reads the data from the file
    root = Tk() # Creates Tkinter window
    root.geometry('750x750') # sets app to 750x750
    root.update() # Updates the dimensions
    root.wm_iconbitmap('Data\\Images\\app_icon.ico')
    root.wm_title('Quotely') # this name is so cringy but hey i'm not creative so yeah... change it when you come up with a better one
    app = Application(root) # loads app
    root.update() # Does it again because why not? Like yes i know it makes the code slower and all that but like again why not, just like go with the flow don't question it
    root.mainloop() # mainloop baby
    read_write('Write') # when the user closes the app it writes all the data is writen
