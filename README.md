Step 1: Install the Required Libraries
Open Command Prompt or PowerShell:

Press Win + R, type cmd, and press Enter (for Command Prompt).
Or press Win + X and select Windows PowerShell.
Ensure pip is installed:

Type pip --version in the command line to check if pip is installed.
If it's not installed, you will need to install pip first (follow the official guide here).
Install the Google API Python Client Libraries: Run the following command to install the required libraries:

bash
Copy code
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
This command will install the necessary Google libraries:

google-api-python-client: To interact with the Google API.
google-auth-httplib2: For handling authentication.
google-auth-oauthlib: For OAuth 2.0 authentication.
Step 2: Verify the Installation
After the installation completes, you can verify that the packages are installed by running:

bash
Copy code
pip list
You should see the libraries google-api-python-client, google-auth-httplib2, and google-auth-oauthlib in the list.

![Screenshot_20241106_222304](https://github.com/user-attachments/assets/a2dce15f-2eaf-4c56-b38e-8e1fea86428c)
