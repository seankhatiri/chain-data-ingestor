async function runPipeline(href, data) {
    console.log(data)
    const response = await fetch(href, {
        method: 'POST',
        body: JSON.stringify(data), // string or object
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const myJson = await response.json(); //extract JSON from the http response
    console.log(myJson);
    // do something with myJson
}

async function stopPipeline(href) {
    const response = await fetch(href, {
        method: 'POST',
        // body: JSON.stringify(data), // string or object
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const myJson = await response.json(); //extract JSON from the http response
    console.log(myJson);
    // do something with myJson
}