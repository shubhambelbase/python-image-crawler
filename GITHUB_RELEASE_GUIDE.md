# How to Publish Your App to GitHub & Create a Download Button

Since you have a vibe-coded Python application, the best way to share it so others can download it easily is to use **GitHub Releases**.

## Step 1: Prepare the Files
1.  Go to your `d:\python\` folder.
2.  Locate the **`ImageCrawler_Dist`** folder (we created this earlier).
3.  Right-click the `ImageCrawler_Dist` folder -> **Send to** -> **Compressed (zipped) folder**.
4.  Rename this zip file to `ImageCrawler_v1.0.zip`.

## Step 2: Upload Code to GitHub
1.  Log in to [GitHub.com](https://github.com).
2.  Click the **+** icon in the top right -> **New repository**.
3.  Name it `Image-Crawler-Pro`.
4.  Active "Add a README file" (optional, but since we have one, uncheck it and we will upload ours).
5.  Click **Create repository**.
6.  Click **uploading an existing file**.
7.  Drag and drop all the files from your `ImageCrawler_Dist` folder (not the zip, the actual files) into the browser.
8.  Commit changes.

## Step 3: Create a "Download" Release
This is the "Pro" way to let people download your app without messing with code.

1.  In your new GitHub repository, find the **Releases** section on the right sidebar.
2.  Click **Create a new release**.
3.  **Choose a tag**: Type `v1.0` and click "Create new tag".
4.  **Release title**: `Image Crawler Pro v1.0`.
5.  **Description**: Paste the content of your `README.md` or write "First vibe coded release."
6.  **Attach binaries**: Drag and drop the **`ImageCrawler_v1.0.zip`** file you created in Step 1 into the box at the bottom.
7.  Click **Publish release**.

## Result
Now, when you send the link to someone, they will see a green **Latest** tag. They can click **Assets** and download the `ImageCrawler_v1.0_Windows.zip` directly!
