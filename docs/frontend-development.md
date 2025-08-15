# Frontend Development

The project uses Node.js for the frontend build tools.

The project uses [SASS](https://sass-lang.com/) for CSS styling and [esbuild](https://esbuild.github.io/) for JavaScript bundling.

## CSS Styling

The project uses [Pico CSS](https://picocss.com/) for styling. It's a minmal setup that you can build on.

When you first run the project you will may notice that no styling is applied. This is because the first time you run the project with `make up` the compiled frontend files are missing, just run the frontend build scripts below and refresh the page.

## JavaScript

The project make no assumption about JavaScript libraries. You can add your own as needed.

## Building the frontend (with reload)

 You can run the build tools with the following commands run from the root of the project:

```bash
nvm use
npm install
npm start
```

`npm start` will watch for file changes and compile the assets.

**Note:** `django-browser-reload` is used to automatically reload the browser when changes are made to the frontend files when debug is enabled.

## Building the frontend (for production)

When you run the `npm start` command, the build tools will watch for changes and reload the browser. This is useful for development but the files are not optimised for production.

When you are ready to deploy the project you will need to build the frontend files for production. You can do this with the following command:

```bash
npm run build
```

If you view any of the frontend files in the `static_compiled` directory you will see that the files are minified and optimised for production.

**Note:** The static files are compiled to the `static_compiled` directory. Depending on your deployment environment you may need to make sure you run the `npm run build` command before deploying. The `static_compiled` directory is not included in the repository becuase it is ignored in the `.gitignore` file, so you will need to remove this line if you want to include the compiled files in the repository.
