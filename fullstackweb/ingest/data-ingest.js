var fs = require('fs');
var _ = require('underscore');

var args = process.argv.slice(2);

var dbFile = 'db.sqlite3';
if(args.length > 0){ dbFile = args[0]; }
var dbExists = fs.existsSync(dbFile);

var dataFile = 'products.json';
if(args.length > 1){ dataFile = args[1]; }
var dataFileExists = fs.existsSync(dataFile);

fs.readFile(dataFile, 'utf8', function(err, data){
  if(err){
    console.log('Error: ' + err);
    return;
  }

  data = JSON.parse(data);
  loadData(data);
});


function loadData(data){
  var sqlite3 = require('sqlite3').verbose();
  var db = new sqlite3.Database(dbFile);

  if(!dbExists){
    console.log('DB file not found');
    return;
  }

  var clearImages = db.prepare("DELETE FROM product_viewer_image WHERE 1=1");
  var clearProd = db.prepare("DELETE FROM product_viewer_product WHERE 1=1");
  
  clearImages.run();
  clearImages.finalize();
  clearProd.run();
  clearProd.finalize();

  var insertProd = db.prepare("INSERT INTO product_viewer_product(id, parent_page_url, merchant_domain, price, image_urls, product_url, last_mod, visit_id, visit_status, page_title, product_title) VALUES (?,?,?,?,?,?,?,?,?,?,?)");

  var insertImage = db.prepare("INSERT INTO product_viewer_image(product_id, url, path, checksum) VALUES(?,?,?,?)");
  
  _.each(data, function(val, idx){
    
    insertProd.run(val._id,
	    val.parent_page_url || '',
	    val.merchant_domain,
	    val.price || '',
	    val.image_urls,
	    val.product_url,
	    val.last_mod,
	    val.visit_id,
	    val.visit_status,
	    val.page_title,
	    val.product_title);
    
    _.each(val.images, function(img, idx2){
      insertImage.run(val._id, img.url, img.path, img.checksum);
    });
  });
  
  insertProd.finalize();
  insertImage.finalize();

}