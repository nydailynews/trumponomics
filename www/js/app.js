var dashboard = {
    config: {},
    update_config: function(config) {
        // Take an external config object and update this config object.
        for ( var key in config )
        {
            if ( config.hasOwnProperty(key) )
            {
                this.config[key] = config[key];
            }
        }
    },
    rando: function(max) {
        // Given a max (integer), return a random number from 0 to the max.
        return Math.floor(Math.random() * max);
    },
    slugify: function (text) {
        // from https://gist.github.com/mathewbyrne/1280286
        return text.toString().toLowerCase()
            .replace(/\s+/g, '-')           // Replace spaces with -
            .replace(/[^\w\-]+/g, '')       // Remove all non-word chars
            .replace(/\-\-+/g, '-')         // Replace multiple - with single -
            .replace(/^-+/, '')             // Trim - from start of text
            .replace(/-+$/, '');            // Trim - from end of text
    },
    load_script: function(url, callback) {
        var s = document.createElement('script');
        s.onload = function() { callback(); };
        s.src = url;
        document.getElementsByTagName('head')[0].appendChild(s);
    },
    get_last_updated: function() {},
    get_next_update: function() {},
    get_lead_item: function() {
        // If a feed has updated today, it should be lead.
        // If more than one feed has updated today, pick a random one of them.
    },
    init: function() {
        this.load_script('_output/all.js', function() { dashboard.data = data; console.log(dashboard, data); });
    }
}; 
dashboard.init();
