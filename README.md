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

