#---------------------------------------------------------------------------
#-- Copyright (c) 2020 Lyaaaaaaaaaaaaaaa
#--
#-- author : Lyaaaaaaaaaaaaaaa
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  -
#--
#-- Changelog:
#--   21/08/2020 Lyaaaaa
#--     - Creation of the file
#--
#--   25/08/2020 Lyaaaaa
#--     - Handler class no longer import Interface (reversed).
#--     - Now import Gtk so it can exit the application.
#--     - Implemented the following methods:
#--       - On_Popover_Menu_About_Clicked
#--       - On_About_Dialog_Close_Button_Clicked
#--       - On_Application_Window_Destroy
#--
#--   27/08/2020 Lyaaaaa
#--     - In On_About_Dialog_Close_Button_Clicked renamed the local variable
#--         "About_Dialog" into "Dialog".
#--     - Implemented the *_Dialog_Cancel_Clicked methods.
#--     - Added todo in the empty methods.
#--     - Added the On_Kanban_Combo_Box_Changed method.
#--     - Added the Scan_Saves method.
#--     - Added the On_Kanban_Combo_Box_Changed method.
#--     - Implemented On_Rename_Dialog_Save_Clicked.
#--     - Added three new variables (attributs) to the class.
#--       - Load, an instance of the Load class,
#--       - Kanban, an instance of the Kanban class,
#--       - action_flag, a flag used to tell the signals what to do.
#--     - Added the Create_Kanban method
#--
#--   31/08/2020 Lyaaaaa
#--     - Scan_Saves becomes Display_Saves because it no longer call Scan_Saves
#--         anymore. Scan_Saves is called on the init of the Load class.
#--
#--   01/08/2020 Lyaaaaa
#--     - Added a Save and File object to the class attributs.
#--     - Implemented Create_Kanban.
#--     - Updated Display_Saves. It no longer directly edits the combo box but
#--         calls Add_Combo_Box_Element which does.
#--     - Created Add_Combo_Box_Element to append element to the combo box.
#--     - Implemented On_Overwrite_Dialog_Yes_Clicked.
#--
#--   02/08/2020 Lyaaaaa
#--     - Removed all related statement to "Rename_Buffer" because it no longer
#--         exist in the interface.
#--     - Replaced the related statement by using "Rename_Dialog_Entry" instead.
#--     - Now import Graphical_Kanban class and create an object of it in
#--         On_Kanban_Combo_Box_Changed.
#--     - Updated On_Kanban_Combo_Box_Changed to create a graphical kanban by
#--         creating an object of the Graphical_Kanban's class.
#--     - Added a Graphical_Kanban attribut to this class (init to None)
#--
#--   18/09/2020 Lyaaaaa
#--     - Added a Temp_Widget_Reference attribut to this class (init to none).
#--         It is used to store a specific widget when a signal can't access it.
#--     - Implemented On_Application_Window_Edit_Kanban_Clicked which is the
#--         signal for the new button on the application header bar to edit the
#--         kanban (for now it's only used to renamed it).
#--     - Implemented On_Edit_Card_Dialog_Save_Clicked when it's used to create
#--         a new card. It only create the graphical card for now.
#--         It still need to edit the kanban object and save the new data.
#--     - Implemented On_Edit_Card_Dialog_Cancel_Clicked.
#--     - Updated On_Rename_Dialog_Save_Clicked to add the case where it is
#--         used to renamed a column.
#--         It still need to edit the kanban object and save the new data.
#--     - Updated On_Kanban_Combo_Box_Changed to call Connect_Column_Buttons
#--         for each Column generated.
#--     - Created and implemented Connect_Column_Buttons.
#--         It connect the two buttons (edit and add) to a clicked signal.
#--     - Created and implemented On_Column_Edit_Clicked signal.
#--     - Created and implemented On_Column_Add_Card_Clicked.
#--
#--   20/09/2020 Lyaaaaa
#--     - Added the following methods:
#--       - Refresh_Interface which simply show all the widgets of the main
#--           window.
#--       - Connect_Card_Buttons (does the same than Connect_Column_Buttons)
#--           but for the card buttons.
#--       - On_Add_Column_Button_Clicked
#--       - On_Card_Edit_Clicked

#--     - Updated On_Kanban_Combo_Box_Changed to updated the name of the kanban
#--         displayed on the new header.
#--     - Fixed On_Edit_Card_Dialog_Save_Clicked, removed
#--         del (Temp_Widget_Reference) which was making an error.
#--     - Updated On_Rename_Dialog_Save_Clicked:
#--       - Added a case where it edits the kanban's title.
#--       - Added a case where it adds a new column.

#--     -
#---------------------------------------------------------------------------

from gi.repository import Gtk

from load             import Load
from file             import File
from save             import Save
from kanban           import Kanban
from graphical_kanban import Graphical_Kanban

class Handler():
  """Link the interface with the backbone and manage the whole application"""

#---------------------------------------------------------------------------
#-- __init__
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  -
#--
#-- Anticipated Changes:
#--  -
#---------------------------------------------------------------------------

  def __init__(self, P_Builder):
    self.Builder          = P_Builder
    self.Load             = Load()
    self.File             = File()
    self.Save             = Save(self.File)
    self.Kanban           = Kanban()
    self.Graphical_Kanban = None

    self.action_flag           = None
    self.Temp_Widget_Reference = None

#---------------------------------------------------------------------------
#-- Scan_Saves
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  - Scan the saves directory.
#--
#-- Anticipated Changes:
#--  -
#---------------------------------------------------------------------------

  def Display_Saves(self):
    Files_Names = self.Load.Get_Files_Names()

    for File_Name in Files_Names:
      self.Add_Combo_Box_Element(File_Name, File_Name)


#---------------------------------------------------------------------------
#-- Create_Kanban
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  -
#--
#-- Anticipated Changes:
#--  -
#---------------------------------------------------------------------------

  def Create_Kanban(self, P_New_Name):
    self.Kanban = Kanban(P_New_Name)

    self.File.Set_Name(P_New_Name)
    self.Save.Set_File(self.File)

    if self.Save.Write_Save(self.Kanban) == True:
      self.Add_Combo_Box_Element(P_New_Name, P_New_Name)

    else:
      Dialog            = self.Builder.get_object("Overwrite_Dialog")
      Label             = self.Builder.get_object("Overwrite_Dialog_Label")
      self.action_flag  = "Overwrite_Kanban"

      Label.set_text("A kanban is already named "
                     + P_New_Name
                     + ". Do you want to overwrite it? There is no coming back")
      Dialog.show()


#---------------------------------------------------------------------------
#-- Add_Combo_Box_Element
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  -
#--
#-- Anticipated Changes:
#--  -
#---------------------------------------------------------------------------
  def Add_Combo_Box_Element(self, P_Element_Text, P_Element_Id):
    Combo_Box   = self.Builder.get_object("Kanban_Combo_Box")
    Combo_Box.append(P_Element_Text, P_Element_Id)


#---------------------------------------------------------------------------
#-- Refresh_Interface
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  -
#--
#-- Anticipated Changes:
#--  -
#---------------------------------------------------------------------------

  def Refresh_Interface(self):
    Interface = self.Builder.get_object("Application_Window")
    Interface.show_all()

  #---------------------------------
  #--          Signals            --
  #---------------------------------

#---------------------------------------------------------------------------
#-- On_Application_Window_Destroy
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  -
#--
#-- Anticipated Changes:
#--  -
#---------------------------------------------------------------------------

  def On_Application_Window_Destroy(self, *args):
    Gtk.main_quit()

#---------------------------------------------------------------------------
#-- On_Application_Window_Add_Kanban_Clicked
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  -
#--
#-- Anticipated Changes:
#--  -
#---------------------------------------------------------------------------

  def On_Application_Window_Add_Kanban_Clicked(self, *args):
    Dialog = self.Builder.get_object("Rename_Dialog")

    Dialog.show()
    self.action_flag = "Add_Kanban"


#---------------------------------------------------------------------------
#-- On_Application_Window_Edit_Kanban_Clicked
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  -
#--
#-- Anticipated Changes:
#--  -
#---------------------------------------------------------------------------

  def On_Application_Window_Edit_Kanban_Clicked(self, *args):
    Dialog = self.Builder.get_object("Rename_Dialog")
    Entry   = self.Builder.get_object("Rename_Dialog_Entry")

    Entry.set_text(self.Kanban.Get_Title())
    Dialog.show()
    self.action_flag = "Edit_Kanban"

#---------------------------------------------------------------------------
#-- On_About_Dialog_Close_Button_Clicked
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  -
#--
#-- Anticipated Changes:
#--  -
#---------------------------------------------------------------------------

  def On_About_Dialog_Close_Button_Clicked(self, *args):
    Dialog = self.Builder.get_object("About_Dialog")
    Dialog.hide()


#---------------------------------------------------------------------------
#-- On_Edit_Card_Dialog_Save_Clicked
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  -
#--
#-- Anticipated Changes:
#--  - Call the methods to edit the Kanban object and save the edited data.
#--  - Implement the case where we edit an existing card.
#---------------------------------------------------------------------------

  def On_Edit_Card_Dialog_Save_Clicked(self, *args):
    Dialog      = self.Builder.get_object("Edit_Card_Dialog")
    Title_Entry = self.Builder.get_object("Edit_Card_Dialog_Title_Entry")
    Buffer      = self.Builder.get_object ("Edit_Card_Dialog_Description_Buffer")
    start       = Buffer.get_start_iter()
    end         = Buffer.get_end_iter()

    Dialog.hide()
    if self.action_flag == "Add_Card":
      Column_Box      = self.Temp_Widget_Reference
      Scrolled_Window = Column_Box.get_children()[0]
      Viewport        = Scrolled_Window.get_child()
      Card_Box        = Viewport.get_child()

      Title           = Title_Entry.get_text()
      Description     = Buffer.get_text(start, end, False)

      Card_Box.add(self.Graphical_Kanban.Add_Card(Title, Description))
      Card_Box.show_all()
      #TODO create the card object and save

    elif self.action_flag == "Edit_Card":
      pass
      #TODO edit the card object and save

    Buffer.set_text("")
    Title_Entry.set_text("")


#---------------------------------------------------------------------------
#-- On_Edit_Card_Dialog_Cancel_Clicked
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  -
#--
#-- Anticipated Changes:
#--  -
#---------------------------------------------------------------------------

  def On_Edit_Card_Dialog_Cancel_Clicked(self, *args):
    Dialog      = self.Builder.get_object("Edit_Card_Dialog")
    Title_Entry = self.Builder.get_object("Edit_Card_Dialog_Title_Entry")
    Buffer      = self.Builder.get_object ("Edit_Card_Dialog_Description_Buffer")

    Buffer.set_text("")
    Title_Entry.set_text("")
    Dialog.hide()


#---------------------------------------------------------------------------
#-- On_Overwrite_Dialog_Yes_Clicked
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  -
#--
#-- Anticipated Changes:
#--  - Add other condition to check for future edit (like edit card or column).
#---------------------------------------------------------------------------

  def On_Overwrite_Dialog_Yes_Clicked(self, *args):
    Dialog = self.Builder.get_object("Overwrite_Dialog")

    if self.action_flag == "Overwrite_Kanban":
      self.Save.Write_Save(self.Kanban, True)
      Dialog.hide()



#---------------------------------------------------------------------------
#-- On_Overwrite_Dialog_Cancel_Clicked
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  -
#--
#-- Anticipated Changes:
#--  -
#---------------------------------------------------------------------------

  def On_Overwrite_Dialog_Cancel_Clicked(self, *args):
    Dialog = self.Builder.get_object("Overwrite_Dialog_Cancel")
    Dialog.hide()


#---------------------------------------------------------------------------
#-- On_Delete_Dialog_Cancel_Clicked
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  -
#--
#-- Anticipated Changes:
#--  -
#---------------------------------------------------------------------------

  def On_Delete_Dialog_Cancel_Clicked(self, *args):
    Dialog = self.Builder.get_object("Delete_Dialog")
    Dialog.hide()


#---------------------------------------------------------------------------
#-- On_Delete_Dialog_Yes_Clicked
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  -
#--
#-- Anticipated Changes:
#--  -
#---------------------------------------------------------------------------

  def On_Delete_Dialog_Yes_Clicked(self, *args):
    pass#TODO


#---------------------------------------------------------------------------
#-- On_Rename_Dialog_Save_Clicked
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  -
#--
#-- Anticipated Changes:
#--  - Call the methods to edit the Kanban object and save the edited data.
#---------------------------------------------------------------------------

  def On_Rename_Dialog_Save_Clicked(self, *args):

    Dialog       = self.Builder.get_object("Rename_Dialog")
    Rename_Entry = self.Builder.get_object("Rename_Dialog_Entry")
    Header_Bar   = self.Builder.get_object("Kanban_Header_Bar")
    new_name     = Rename_Entry.get_text()

    if   self.action_flag == "Add_Kanban":
      self.Create_Kanban(new_name)

    elif self.action_flag == "Edit_Kanban":
      self.Kanban.Set_Title(new_name)
      Header_Bar.set_title(new_name)

    elif self.action_flag == "Rename_Column":
      Column_Label = self.Temp_Widget_Reference

      del self.Temp_Widget_Reference
      Column_Label.set_markup(  "<b> <big>"
                              + Rename_Entry.get_text()
                              + "</big> </b>")
      #TODO Edit the column's title from the Kanban object
      #TODO Add a call to save the data into the file

    elif self.action_flag == "Add_Column":
      Column = self.Graphical_Kanban.Add_Column(new_name)

      self.Kanban.Add_Column(new_name)
      self.Refresh_Interface()
      self.Connect_Column_Buttons(Column)

    Rename_Entry.set_text("")
    Dialog.hide()

#---------------------------------------------------------------------------
#-- On_Rename_Dialog_Cancel_Clicked
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  -
#--
#-- Anticipated Changes:
#--  -
#---------------------------------------------------------------------------

  def On_Rename_Dialog_Cancel_Clicked(self, *args):
    Dialog        = self.Builder.get_object("Rename_Dialog")
    Rename_Entry  = self.Builder.get_object("Rename_Dialog_Entry")

    Rename_Entry.set_text("")
    Dialog.hide()

#---------------------------------------------------------------------------
#-- On_Popover_Menu_Help_Clicked
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  -
#--
#-- Anticipated Changes:
#--  -
#---------------------------------------------------------------------------

  def On_Popover_Menu_Help_Clicked(self, *args):
    pass#TODO

#---------------------------------------------------------------------------
#-- On_Popover_Menu_Preferences_Clicked
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  -
#--
#-- Anticipated Changes:
#--  -
#---------------------------------------------------------------------------

  def On_Popover_Menu_Preferences_Clicked(self, *args):
    pass#TODO

#---------------------------------------------------------------------------
#-- On_Popover_Menu_About_Clicked
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  -
#--
#-- Anticipated Changes:
#--  -
#---------------------------------------------------------------------------

  def On_Popover_Menu_About_Clicked(self, *args):
    About_Dialog = self.Builder.get_object("About_Dialog")
    About_Dialog.show()


#---------------------------------------------------------------------------
#-- On_Kanban_Combo_Box_Changed
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  - What happens when you select a kanban.
#--
#-- Anticipated Changes:
#--  -
#---------------------------------------------------------------------------

  def On_Kanban_Combo_Box_Changed(self, *args):
    Combo_Box   = self.Builder.get_object("Kanban_Combo_Box")
    Content_Box = self.Builder.get_object("Content_Box")
    Header_Bar  = self.Builder.get_object("Kanban_Header_Bar")
    active_id   = Combo_Box.get_active_id()

    if active_id != "placeholder":
      del (self.Graphical_Kanban)
      self.Kanban           = self.Load.Load_Save_File(active_id)
      self.Graphical_Kanban = Graphical_Kanban(self.Kanban, Content_Box)
      Header_Bar.set_title(self.Kanban.Get_Title())

    for Column_Box in Content_Box.get_children():
      self.Connect_Column_Buttons(Column_Box)
      # TODO Call Connect_Card_Buttons method


#---------------------------------------------------------------------------
#-- Connect_Column_Buttons
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  - Create the signal on_clicked and handler for each column's edit button.
#--
#-- Anticipated Changes:
#--  -
#---------------------------------------------------------------------------

  def Connect_Column_Buttons(self, P_Column_Box):
    Column_Header           = P_Column_Box.get_children()[1]
    Header_Items            = Column_Header.get_children()
    Column_Label            = Header_Items[0]
    Column_Edit_Button      = Header_Items[1]
    Column_Add_Card_Button  = Header_Items[2]

    Column_Edit_Button.connect    ("clicked",
                                   self.On_Column_Edit_Clicked,
                                   Column_Label)
    Column_Add_Card_Button.connect("clicked",
                                   self.On_Column_Add_Card_Clicked,
                                   P_Column_Box)


#---------------------------------------------------------------------------
#-- Connect_Card_Buttons
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  - Create the signal on_clicked and handler for each column's edit button.
#--
#-- Anticipated Changes:
#--  -
#---------------------------------------------------------------------------
  def Connect_Card_Buttons(self, P_Card_Box):
    Card_Header      = P_Card_Box.get_children()[0]
    Card_Edit_Button = Card_Header.get_children()[1]

    Card_Edit_Button.connect("clicked",
                             self.On_Card_Edit_Clicked,
                             P_Card_Box)


#---------------------------------------------------------------------------
#-- On_Column_Edit_Clicked
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  - Display Rename_Dialog
#--
#-- Anticipated Changes:
#--  -
#---------------------------------------------------------------------------

  def On_Column_Edit_Clicked(self, P_Edit_Button, P_Column_Label):
    Dialog       = self.Builder.get_object("Rename_Dialog")
    Rename_Entry = self.Builder.get_object("Rename_Dialog_Entry")

    Rename_Entry.set_text(P_Column_Label.get_text())

    Dialog.show()
    self.action_flag           = "Rename_Column"
    self.Temp_Widget_Reference = P_Column_Label


#---------------------------------------------------------------------------
#-- On_Column_Add_Card_Clicked
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  -
#--
#-- Anticipated Changes:
#--  -
#---------------------------------------------------------------------------

  def On_Column_Add_Card_Clicked(self, P_Add_Button, P_Column_Box):
    Dialog = self.Builder.get_object("Edit_Card_Dialog")

    Dialog.show()
    self.action_flag = "Add_Card"
    self.Temp_Widget_Reference = P_Column_Box


#---------------------------------------------------------------------------
#-- On_Add_Column_Button_Clicked
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  -
#--
#-- Anticipated Changes:
#--  - Check if a kanban is already created or selected
#---------------------------------------------------------------------------

  def On_Add_Column_Button_Clicked(self, *args):
    Rename_Dialog    = self.Builder.get_object("Rename_Dialog")
    self.action_flag = "Add_Column"

    Rename_Dialog.show()


#---------------------------------------------------------------------------
#-- On_Card_Edit_Clicked
#--
#-- Portability Issues:
#--  -
#--
#-- Implementation Notes:
#--  -
#--
#-- Anticipated Changes:
#--  -
#---------------------------------------------------------------------------

  def On_Card_Edit_Clicked(self, P_Edit_Button, P_Card_Box):
    Edit_Dialog = self.Builder.get_object("Edit_Card_Dialog")

    self.Temp_Widget_Reference = P_Card_Box
    Edit_Dialog.show()
