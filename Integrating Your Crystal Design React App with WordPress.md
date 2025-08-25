# Integrating Your Crystal Design React App with WordPress

This guide will walk you through the process of embedding your Crystal Design React app into WordPress using the ReactPress plugin.

## Required Free Tools

1. **ReactPress Plugin** - A free WordPress plugin that allows you to embed React apps into WordPress pages
2. **WordPress** - Your WordPress installation (local for development, and a hosting provider for production)
3. **Node.js and npm** - For building your React application

## Preparing Your React App for WordPress

### Step 1: Adjust the React App for WordPress Compatibility

Your Crystal Design React app needs a few adjustments to work properly with WordPress:

1. **Update the homepage in package.json**:
   Open your `package.json` file and add:
   ```json
   "homepage": ".",
   ```
   This ensures all asset paths are relative rather than absolute.

2. **Update Router Configuration** (if using React Router):
   In your `App.tsx` file, update the Router to use a basename that matches your WordPress page slug:
   ```jsx
   <Router basename="/crystal-design">
     {/* Your routes */}
   </Router>
   ```

3. **Ensure Public Assets are Referenced Correctly**:
   Update all asset references to use relative paths:
   ```jsx
   // Instead of
   <img src="/images/book-cover.jpg" />
   
   // Use
   <img src={`${process.env.PUBLIC_URL}/images/book-cover.jpg`} />
   ```

### Step 2: Build Your React App

1. Run the build command to create a production-ready version:
   ```bash
   npm run build
   ```

2. This will create a `build` folder containing all the necessary files for deployment.

## WordPress Integration Steps

### Step 1: Install WordPress

If you don't already have WordPress installed:

1. **Local Development**: Use a local development environment like [LocalWP](https://localwp.com/) (free)
2. **Production**: Choose a WordPress hosting provider like Bluehost, SiteGround, or DreamHost

### Step 2: Install and Configure ReactPress Plugin

1. Log in to your WordPress admin dashboard
2. Go to **Plugins > Add New**
3. Search for "ReactPress"
4. Click **Install Now** and then **Activate**

### Step 3: Create a New React App in ReactPress

1. In your WordPress admin, click on **ReactPress** in the sidebar
2. Fill out the form to create a new app:
   - **Name**: `crystal-design` (use this exact name)
   - **Page Slug**: Choose a URL path where your app will be accessible (e.g., `crystal-design`)
   - **Type**: Select "Deploy an already built app (Usually on a server)"
   - Click **Create React App**

### Step 4: Upload Your React App Build

1. Locate your app directory in WordPress:
   - The ReactPress admin will show the path (typically something like `.../wp-content/plugins/reactpress/apps/crystal-design`)
2. Upload the contents of your React app's `build` folder to this directory
   - You can use FTP, cPanel File Manager, or SSH to upload the files
   - Make sure to preserve the directory structure

### Step 5: Test Your Integration

1. Visit your WordPress site at the URL slug you specified (e.g., `https://your-site.com/crystal-design`)
2. Verify that your Crystal Design React app loads correctly within WordPress
3. Test all functionality to ensure everything works as expected

## Troubleshooting Common Issues

### White Screen or App Not Loading

1. Check browser console for errors
2. Verify that all asset paths are relative
3. Ensure the ReactPress plugin is properly activated
4. Check file permissions on the uploaded build files

### Routing Issues

1. Make sure you've configured React Router with the correct basename
2. Check that your WordPress permalink settings are set to "Post name" (Settings > Permalinks)

### Asset Loading Problems

1. Verify that all assets are properly referenced with relative paths
2. Check that all required files were uploaded to the correct location

## Maintaining Your App

When you need to update your React app:

1. Make changes to your React code
2. Rebuild the app (`npm run build`)
3. Upload the new build files to your WordPress server, replacing the old files

## Additional Resources

- [ReactPress Plugin Documentation](https://wordpress.org/plugins/reactpress/)
- [ReactPress Tutorial](https://dev.to/rockiger/easily-embed-react-apps-into-wordpress-with-reactpress-plugin-7p8)
- [React Router Documentation](https://reactrouter.com/en/main)
