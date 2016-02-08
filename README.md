# item-catalog
In this project, I will be developing a web application that provides a list of items within a variety of categories and integrate third party user registration and authentication. Authenticated users should have the ability to post, edit, and delete their own items. I will be creating this project essentially from scratch, no templates have been provided for me. This means free reign over the HTML, the CSS, and the files that include the application itself utilizing Flask.

Getting Started

Before we begin coding, there are several steps that you should take to make sure that you have everything downloaded in order to run your future web application.
1. Install Vagrant and VirtualBox if you have not done so already. Instructions on how to do so can be found on the websites as well as in the course materials.

2. Clone the https://github.com/Nehal90/item-catalog repository.

3. Launch the Vagrant VM (by typing vagrant up in the directory fullstack/vagrant from the
terminal). You can find further instructions on how to do so here .

4. The Flask application locally is in the /vagrant/item-catalog directory (which will automatically be synced to /vagrant/item-catalog within the VM).

5. Run your application within the VM by typing python /vagrant/item-catalog/project.py

6. Access and test the application by visiting http://localhost:5000 http://localhost:your-vm-port-number or locally on your browser.

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
