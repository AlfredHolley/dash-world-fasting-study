window.dash_clientside = {
    clientside: {
        update_dropvalue: function(dropdown_id,...timestamps) {
            timestamps = timestamps.map(timestamp => timestamp || 0);
            var highestTimestamp = Math.max(...timestamps);
            var clicked_id = null;

            for (var i = 1; i <= timestamps.length; i++) {
                if (timestamps[i - 1] === highestTimestamp) {
                    clicked_id = dropdown_id +'-menu-div-' + i;
                    break;
                }
            }
            console.log('Clicked ID:', clicked_id);

            if (clicked_id) {
                var clickedContent = document.getElementById(clicked_id);

                if (clickedContent) {
                    var trimmedText = clickedContent.textContent.trim();

                    console.log('Clicked content:', trimmedText);
                    var contentWithoutSuffix = trimmedText.replace(/:.*/, '').trim();
                    console.log('Clicked content:', contentWithoutSuffix);

                    return contentWithoutSuffix;
                }
            }
            return null;
        },

        div_creator: function(param, data) {
            function getBackgroundColor(value) {
                // Map the absolute value to a color intensity between 0 (white) and 255 (red)
                var intensity = Math.floor(255 * Math.abs(value));
                return 'rgba(0, 0, 255, ' + intensity / 400 + ')';
            }

            var filteredDataDict = {};
            for (var key in data[0][param]) {
                var value = parseFloat(data[0][param][key]).toFixed(2);
                if (!isNaN(value) && value !== null && value !== "None") {
                    filteredDataDict[key] = value;
                }
            }

            var sortedDataDict = Object.fromEntries(Object.entries(filteredDataDict).sort((a, b) => Math.abs(b[1]) - Math.abs(a[1])));

            var contents = [];
            var styles = [];

            for (var i = 0; i < 44; i++) {
                if (i < Object.keys(sortedDataDict).length) {
                    var content = Object.entries(sortedDataDict)[i];
                    contents.push(content[0] + ' : ' + content[1]);
                    styles.push({'background-color': getBackgroundColor(content[1])});
                } else {
                    contents.push(null);
                    styles.push({'display': 'none'});
                }
            }

            return contents.concat(styles);
        }
    }
};

