var http = require('http');
var formidable = require('formidable');
var fs = require('fs');

http.createServer(function (req, res) {
  if (req.url == '/fileupload') {
    var form = new formidable.IncomingForm();
    form.parse(req, function (err, fields, files) {
      var oldpath = files.filetoupload.path;
      var newpath = '/home/suryo/Desktop/HackUTA_py/Image_in/' + files.filetoupload.name;
      fs.rename(oldpath, newpath, function (err) {
        if (err) throw err;
        res.write('File uploaded and moved!');
        res.end();
      });
 });
  } else {
    res.writeHead(200, {'Content-Type': 'text/html'});
	  res.write('<head>');
   	  res.write('<title>Disaster Mitigation</title>');
	  res.write('<meta charset="utf-8">');
	  res.write('<meta name="viewport" content="width=device-width, initial-scale=1">')
	  res.write('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">')
	  res.write('<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>')
	  res.write('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>')
	  res.write('</head>');
    res.write('</br></br></br>')
    res.write('<form action="fileupload" method="post" enctype="multipart/form-data">');
    res.write('<center><input type="file" name="filetoupload" class="btn btn-primary"><br></center>');
    res.write('<center><input type="submit"  style="border:1px solid" class="btn btn-primary"></center>');
    res.write('</form>');
    return res.end();
  }
}).listen(8080); 
