# item-catalog
In this project, I will be developing a web application that provides a list of items within a variety of categories and integrate third party user registration and authentication. Authenticated users should have the ability to post, edit, and delete their own items. I will be creating this project essentially from scratch, no templates have been provided for me. This means free reign over the HTML, the CSS, and the files that include the application itself utilizing Flask.

Getting Started

Before we begin coding, there are several steps that you should take to make sure that you have everything downloaded in order to run your future web application.
1. Install Vagrant and VirtualBox if you have not done so already. Instructions on how to do so can be found on the websites as well as in the course materials.

2. Clone the fullstacknanodegreevm repository . There is a catalog folder provided for you, but no files have been included. If a catalog folder does not exist, simply create your own inside of the vagrant folder.

3. Launch the Vagrant VM (by typing vagrant up in the directory fullstack/vagrant from the
terminal). You can find further instructions on how to do so here .

4. Write the Flask application locally in the /vagrant/catalog directory (which will automatically be synced to /vagrant/catalog within the VM). Name it application.py.

5. Run your application within the VM by typing python /vagrant/catalog/application.py
into the Terminal. If you named the file from step 4 as something other than application.py, in the above command substitute in the file name on your computer.

6. Access and test your application by visiting http://localhost:8000 locally on your browser.

Accessing JSON End Points:
There are three JSON End poits avaiable. Theya are as followed:
1. '../categories/JSON')
Returns a JSON list of all the categories in the catalog.

2. '../categories/<int:category_id>/items/JSON')
Returns a JSON list of all the items available within a category.

Example:

'http://localhost:5000/categories/2/items/JSON' returns:

{
  "CategoryItems": [
    {
      "category": 2,
      "description": "A high or low shoe, usually of fabric such as canvas, with a rubber or synthetic sole",
      "id": 7,
      "name": "Sneakers"
    },
    {
      "category": 2,
      "description": "A sleeveless shirt is a shirt manufactured without sleeves, or one whose sleeves have been cut off.",
      "id": 8,
      "name": "Sleeveless Shirt"
    },
    {
      "category": 2,
      "description": "A circular band of metal, wood, or similar material, especially one used for binding the staves of barrels or forming part of a framework.",
      "id": 9,
      "name": "Hoop"
    },
    {
      "category": 2,
      "description": "A board placed at or forming the back of something, such as a collage or piece of electronic equipment.",
      "id": 10,
      "name": "Backboard"
    }
  ]
}



3. '../categories/<int:category_id>/items/<int:item_id>/JSON') 

Example:

 'http://localhost:5000/categories/2/items/2/JSON' returns:

{
  "CategoryItem": {
    "category": 1,
    "description": "The shirt worn by players.",
    "id": 2,
    "name": "Jersey"
  }
}

Returns a JSON list for a specific item.
