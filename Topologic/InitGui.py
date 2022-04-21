# * This file is part of Topologic software library.
# * Copyright(C) 2021, Cardiff University and University College London
# * 
# * This program is free software: you can redistribute it and/or modify
# * it under the terms of the GNU Affero General Public License as published by
# * the Free Software Foundation, either version 3 of the License, or
# * (at your option) any later version.
# * 
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU Affero General Public License for more details.
# * 
# * You should have received a copy of the GNU Affero General Public License
# * along with this program. If not, see <https://www.gnu.org/licenses/>.

import os

class TopologicWorkbench (Workbench):

    def __init__(self):
        self.__class__.MenuText = "Topologic"
        self.__class__.ToolTip = (
            "Topologic is a software development kit and plug-in that enables logical, hierarchical and topological representation of spaces and entities"
        )
        self.__class__.Icon = os.path.join(FreeCAD.__path__[2],"Topologic","Resources","icons","TopologicWorkbench.svg")

    def Initialize(self):
        """This function is executed when FreeCAD starts"""
        import TPVertexGui # import here all the needed files that create your FreeCAD commands
        self.list = ["TPVertices"] # A list of command names created in the line above
        self.appendToolbar("Topologic Commands",self.list) # creates a new toolbar with your commands
        self.appendMenu("Topologic",[]) # creates a new menu
        self.appendMenu(["Topologic","Vertex"],self.list) # appends a submenu to an existing menu

    def Activated(self):
        """This function is executed when the workbench is activated"""
        return

    def Deactivated(self):
        """This function is executed when the workbench is deactivated"""
        return

    def ContextMenu(self, recipient):
        """This is executed whenever the user right-clicks on screen"""
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu("My commands",self.list) # add commands to the context menu

    def GetClassName(self): 
        # This function is mandatory if this is a full python workbench
        # This is not a template, the returned string should be exactly "Gui::PythonWorkbench"
        return "Gui::PythonWorkbench"
  
Gui.addWorkbench(TopologicWorkbench())