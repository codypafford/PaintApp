from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import messagebox


pic_list = []


class Paint:
    global pic_list
    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()
        self.root.title("Codys Paint Application")
       
        # pen button
        self.pen_button = Button(self.root, text='pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)
        self.pen_button.config(bg = "ivory4")
        # brush button
        self.brush_button = Button(self.root, text='brush', command=self.use_brush)
        self.brush_button.grid(row=0, column=1)
        self.brush_button.config(bg = "ivory4")
        # color button
        self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=2)
        self.color_button.config(bg = "ivory4")
        # eraser button
        self.eraser_button = Button(self.root, text='eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=3)
        self.eraser_button.config(bg = "ivory4")
        # choose size button
        self.choose_size_button = Scale(self.root, from_=4, to=18, orient=HORIZONTAL)
        self.choose_size_button.grid(row=1, column=0)
        # import image button
        self.import_img_button = Button(self.root, text='import image', command=self.import_image)
        self.import_img_button.grid(row=0,column=5)
        # edit box for width/height
        self.img_resize = Entry(self.root, width=8)
        self.img_resize.grid(row=0, column=4)
        self.var_img_size = StringVar()
        # center, ne, nw, etc.. button
        variable = StringVar(self.root)
        variable.set("center") # default value
        self.w = OptionMenu(self.root, variable, "center", "nw", "n", "ne", "w", "e", "sw", "s", "se", command=self.getOptionMenuValue)
        self.w.grid(row=1, column=5)
        # width/height label
        self.label = Label( self.root, textvariable=self.var_img_size, relief=RAISED )
        self.var_img_size.set("width,height")
        self.label.grid(row=1,column=4)
        # canvas 
        self.c = Canvas(self.root, bg='white', width=900, height=900)
        self.c.grid(row=2, columnspan=6)
        # pafford image
      #  filename = PhotoImage(file = "C:\\Users\cpafford\Desktop\Paint\pafford.py")
      #  self.image = self.c.create_image(60, 30, image=filename)
      #  pic_list.append(self.image)

        # self.c.tag_bind(self.image, '<Button1-Motion>', self.move)
        # self.c.tag_bind(self.image, '<ButtonRelease-1>', self.release)

        # paint image
      #  filename1 = PhotoImage(file = "/home/codyp/Desktop/Paint/paint.png")
      #  self.image2 = self.c.create_image(60, 60, image=filename1)
      #  pic_list.append(self.image2)



        self.setup()
        self.root.mainloop()


     # move images drag and drop    
     # change image2 to whatever was clicked last
    def move(self, event):
        print("moving")
        if self.move_flag:
            new_xpos, new_ypos = event.x, event.y
             
            self.c.move(self.selected_image,
                new_xpos-self.mouse_xpos ,new_ypos-self.mouse_ypos)
             
            self.mouse_xpos = new_xpos
            self.mouse_ypos = new_ypos
        else:
            self.move_flag = True
            self.c.tag_raise(self.selected_image)
            self.mouse_xpos = event.x
            self.mouse_ypos = event.y
 
    def release(self, event):
        self.move_flag = False

    def getOptionMenuValue(self,value):
        self.option_menu = value

    def setup(self):
        global button_list
        self.option_menu = "center"
        self.brush_on = False
        self.pen_button.config(bg = 'deep sky blue')
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)
       # self.selected_image = pic_list[-1]

        try:
            if self.selected_image:
                print("yessssss")
                self.c.tag_bind(self.selected_image, '<Button1-Motion>', self.move)
                self.c.tag_bind(self.selected_image, '<ButtonRelease-1>', self.release)
        except:
            pass
        self.move_flag = False
        button_list = [self.pen_button, self.brush_button, self.eraser_button]

    def use_pen(self):
        self.activate_button(self.pen_button)
        self.brush_on = False


    def use_brush(self):
        self.activate_button(self.brush_button)
        self.brush_on = True

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def import_image(self):
        global pic_list
       
        try:
            width = self.img_resize.get().split(",")[0]
            height = self.img_resize.get().split(",")[1]
            width = int(width)
            height = int(height)
        except:
            messagebox.showinfo("Message", "Enter a width and a height seperated by a comma") 
            return  


        sel_pic =  filedialog.askopenfilename(initialdir = "/",title = "Select image",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        image = Image.open(str(sel_pic))
        image = image.resize((width, height), Image.ANTIALIAS)
        tkImage = ImageTk.PhotoImage(image)
      #  pic_list.append(tkImage)

        self.c.create_image(400, 400, image = tkImage, anchor = self.option_menu)

        self.img4 = tkImage #Reference
        self.selected_image = self.img4
        pic_list.append(self.img4)

        self.c.tag_bind(self.selected_image, '<Button1-Motion>', self.move)
        self.c.tag_bind(self.selected_image, '<ButtonRelease-1>', self.release)
        self.move_flag = False



    def activate_button(self, some_button, eraser_mode=False):
        some_button.config(bg="deep sky blue")
        some_button.config(relief=SUNKEN)
        for button in button_list:
            if not button == some_button:
                button.config(bg='ivory4')

        self.active_button = some_button

        self.eraser_on = eraser_mode


    def paint(self, event):
        # print(event.x)
        # print(event.y)
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        if self.brush_on:
            if self.old_x and self.old_y:
                self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                                   width=self.line_width, fill=paint_color,
                                   capstyle=ROUND, smooth=TRUE, splinesteps=36)
        else:
            if self.old_x and self.old_y:
                self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                                   width=self.line_width, fill=paint_color,
                                   capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None


if __name__ == '__main__':
    Paint()