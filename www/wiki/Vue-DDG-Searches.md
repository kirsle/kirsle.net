# DuckDuckGo Search Queries for Vue Multi-site Config

## Goal

Using vue-cli, set up a project that allows for two distinct web apps to exist
in the same repository together: a "main" site and an "admin" site.

Each site would have a distinct top-level Vue app (entry point) and a distinct
"public/" folder of assets to copy into each site. Each site would have some Vue
components specific to itself, but also be able to share components common to
both sites.

## Searches

All searches done using [DuckDuckGo](https://duckduckgo.com/)

1. Search `man vue-cli-service` (attempting to find the manual page for the
   vue-cli-service command, to check for CLI options)
  * Landed on [CLI Service | Vue CLI 3](https://cli.vuejs.org/guide/cli-service.html)
  * Didn't find anything useful from this page.
2. Went to Vue CLI homepage to learn how to install vue-cli and create a
   hello-world app of my own, so that I could run
   `./node_modules/.bin/vue-cli-service --help` and see the man page that
   way. Didn't find any CLI options that would configure the public folder
   path in the man page.
3. Search `vue-cli public folder path`
  * Landed on [HTML and Static Assets | Vue CLI 3](https://cli.vuejs.org/guide/html-and-static-assets.html)
  * First paragraph says: "The file public/index.html is a template that
    will be processed with [html-webpack-plugin](https://github.com/jantimon/html-webpack-plugin)"
  * So I knew the part of vue-cli (html-webpack-plugin) responsible for this
    feature. But how does vue-cli configure it? There is no webpack.config.js,
    and I searched my hello-world codebase for the word "public" and didn't see
    any explicit configuration anywhere for it.
4. Search `vue-cli html-webpack-plugin settings`
  * Landed on [Working with Webpack | Vue CLI 3](https://cli.vuejs.org/guide/webpack.html)
  * Found my first hint on how you can create a `vue.config.js` and customize
    options to the html-webpack-plugin (under "Modifying Options of a Plugin"):

    ```javascript
// vue.config.js
module.exports = {
  chainWebpack: config => {
    config
      .plugin('html')
      .tap(args => {
        args[0].template = '/Users/username/proj/app/templates/index.html'
        return args
      })
  }
}
    ```

  * This let you override the "public/index.html" path with a custom path, and
    was half of the final solution. (Other half is getting the _other_ "public/*"
    files to be copied into your dist folder!)
5. Seeing mention of publicPath in places, searched `vue publicPath config`
  * Landed on [Configuration Reference | Vue CLI 3](https://cli.vuejs.org/config/)
    and saw mentions of a "publicPath" variable, but it turned out this
    wasn't what I wanted. publicPath is the HTTP URI of your website root, default
    is "/", if you changed it to e.g. "/custom-public" then the index.html of your
    dist/ output references files as e.g. `<script src="/custom-public/app.js">`
6. Searched `vue-cli multiple public folders`
  * Found [Change public folder in vue-cli project](https://stackoverflow.com/questions/49278322/change-public-folder-in-vue-cli-project)
    from StackOverflow. Code snippets in the responses were similar to the one
    above from step 4, changing the path of the index.html but not getting the
    other files.
  * Found a GitHub issue on vue-cli for [Make public folder path configurable](https://github.com/vuejs/vue-cli/issues/3184).
    **This was the solution! 🎊** Found a code snippet for my vue.config.js that
    would do what I wanted and use a differently-named folder for the public files:

    ```javascript
// vue.config.js
const path = require('path')

const publicDir = 'assets/html';

module.exports = {
    chainWebpack: config => {
        config
            .plugin('html')
            .tap(args => {
                args[0].template = path.resolve(publicDir + '/index.html');
                return args
            })

        config
            .plugin('copy')
            .tap(([pathConfigs]) => {
                pathConfigs[0].from = path.resolve(publicDir);
                return [pathConfigs]
            })
    }
}
    ```

  * Now I just needed to make it _configurable_ so you could `npm run build-admin`
    to build an "admin site" or `npm run build-main` to build a "main" site, each
    using its own public folder.
* Searches: `vue.config.js runtime options`, `vue-cli multiple vue.config.js`
  and `vue.config.js config variables` before landing on
  [Environment Variables and Modes | Vue CLI 3](https://cli.vuejs.org/guide/mode-and-env.html#modes)
  * Solution: create .env files that define variables, use the `--mode` option of
    `vue-cli-service` to specify the .env file to load, and the variables are
    available inside your vue.config.js at the `process.env` variable.

## Source files I ended up with

vue.config.js:

```javascript
let PUBLIC_PATH = process.env.VUE_SITE_NAME === "admin" ? "custom-public" : "public";

module.exports = {
    chainWebpack: config => {
      config
        .plugin('html')
        .tap(args => {
          args[0].template = PUBLIC_PATH + '/index.html'
          return args
        })

      config
        .plugin('copy')
        .tap(([pathConfigs]) => {
            pathConfigs[0].from = PUBLIC_PATH;
            return [pathConfigs]
        })
    }
}
```

package.json npm run scripts:

```javascript
  "scripts": {
    "serve": "vue-cli-service serve",
    "build-admin": "vue-cli-service build --mode admin --dest admin-dist ./src/admin/index.js",
    "build": "vue-cli-service build --mode main --dest dist ./src/main/index.js",
    "lint": "vue-cli-service lint"
  },
```

.env config files:

```
# .env.admin
VUE_SITE_NAME=admin

# .env.main
VUE_SITE_NAME=main
```

So:

* `npm build` would output the site to the default dist/ folder, use
  ./src/main/index.js as the entry point (instead of default src/main.js from
  a default vue-cli project) and use the default public/ folder.
* `npm build-admin` would output the site to admin-dist/ (so as not to overwrite
  the dist/ for the main site), use ./src/admin/index.js as entry point and use
  the folder "custom-public/" instead of default public/ to get its index.html and
  static assets.
