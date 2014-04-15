define('product-viewer', ['jquery', 'underscore', 'xutil', 'xmvvm', 'product-viewer-init', 'bootstrap'],
	   function($, _, $x, mvvm, init){
	'use strict';
	var exports = {};
	exports.ImageRef = mvvm.Model.extend({
	
	});
	
	exports.ImageRefCollection = mvvm.Collection.extend({
		model: exports.ImageRef
	});
	
	exports.Product = mvvm.Model.extend({
		fields: {
			id: String,
			parent_page_url: String,
			merchant_domain: String,
			price: String,
			image_urls: String,
			images: exports.ImageRefCollection,
			product_url: String,
			last_mod: Date,
			visit_id: String,
			visit_status: String,
			page_title: String,
			product_title: String
		}
	});

	exports.ProductCollection = mvvm.Collection.extend({
		model: exports.Product
	});
	
	exports.ProductQueryResults = mvvm.Model.extend({
		fields: {
			count: Number,
			next: String,
			previous: String,
			results: exports.ProductCollection
		}
	});
	
	exports.ProductViewer = mvvm.ViewModel.extend({
		view: 'template-products',
		fields: {
			model: exports.ProductQueryResults,
			rows: mvvm.Collection,
			pages: mvvm.Collection,
			page: Number,
			query: String
		},
		defaults: {
			page: 1,
			query: null
		},
		initialize: function(){
			var t=this;
			t.rows( new mvvm.Collection() );
			t.pages( new mvvm.Collection() );
			_.bindAll(t, 'totalPages', 'updateRows', 'search', 'loadItems', 'bindModel', 'getItems', 'getPagesForPaging', 'notFirst', 'notLast', 'isCurrentPage');
			t.on('change:model', t.bindModel);
			t.on('change:model', t.updateRows);
			t.on('change:query', function(){
				//make sure we trigger updates for page changes
				t.page(0);
				t.page(1);
			});
			$('form[role="search"]').on('keyup', t.search);
		},
		totalPages: function(){
			var t = this;
			return Math.ceil((t.model().count() - 1) / 20 + 1);
		},
		bindModel: function(){
			
		},
		updateRows: function(){
			var t=this;
			//Creates dummy models to represent each row.
			//This is so that the template can get change events when
			//the number of rows changes.
			while(t.model().results().length / 4.0 > t.rows().length){
				t.rows().add( new mvvm.Model({
					index: t.rows().length
				}) );
			}
			
			
			while(t.totalPages() > t.pages().length){
				t.pages().add( new mvvm.Model({
					index: t.pages().length + 1
				}) );
			}
		},
		getItems: function(row){
			var t=this;
			return t.model().results().slice(row.get('index'), row.get('index') + 4);
		},
		getPagesForPaging: function(){
			var t=this;
			
			
			var start = Math.max(1, t.page() - 3);
			var end = Math.min(t.totalPages(), t.page() + 3);
			return t.pages().filter(function(val){
				return val.get('index') >= start && val.get('index') < end;
			});
		},
		search: function(evt, ui){
			var t=this;
			//evt.preventDefault();
			
			var q = $('form[role="search"] input[name="search"]').val();
			if(q !== t.query()){
				t.page(1);
				t.query(q);
				t.loadItems();
				window.product_router.navigate('/page/1/', {trigger: false});
			}
			
			
			
			//return false;
		},
		
		loadItems: function(){
			var t=this;
			return new Promise( function(resolve, reject){
							
				retrieveListData(t.query(), t.page()).then(function(data){
					var model = t.model();
					if(model === null || model === undefined){
						t.model( new exports.ProductQueryResults(data, {parse: true}) );
					}else{
						var result = new exports.ProductQueryResults(data, {parse: true});
						t.rows().reset([]);
						t.pages().reset([]);
						t.model().results(result.results());
						t.model().count(result.count());
						
						t.updateRows();
					}
					resolve();				
				}, function(err){
					reject(err);
				});
			});
		},
		//helper Filter functions
		notFirst: function(val){
			return val > 1;
		},
		notLast: function(val){
			var t=this;
			return val < t.totalPages();
		},
		isCurrentPage: function(val){
			return val == this.page();
		}
		
	});
	
	var retrieveListData = function(query, page){
		var params = [], url = init.listUrl;
		if(query !== undefined && query !== null && query !== ''){
			params.push('q=' + query);
		}
		if(page !== 1){
			params.push('page=' + page);
		}
		for(var i=0; i<params.length; i++){
			if(i===0){
				url += '?';
			}else{
				url += '&';
			}
			url += params[i];
		}
		return new Promise(function(resolve, reject){
			$.ajax({
				type: 'GET',
				dataType: 'json',
				url: url				
			}).success(function(data){
				resolve(data);
			}).error(function(){
				reject();
			});
		});
	};
	
	retrieveListData = _.memoize(retrieveListData, function(query, page){
		return (query || '').toString() + '::' + page.toString();
	});
	
	return exports;
});