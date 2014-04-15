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
			_.bindAll(t, 'updateRows', 'search', 'loadItems', 'bindModel', 'getItems', 'getPagesForPaging', 'notFirst', 'notLast', 'isCurrentPage');
			t.on('change:model', t.bindModel);
			t.on('change:model', t.updateRows);
			$('form[role="search"]').on('submit', t.search);
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
			
			var totalPages = (t.model().count() - 1) / 20 + 1;
			while(totalPages > t.pages().length){
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
			var totalPages = (t.model().count() - 1) / 20 + 1;
			totalPages = Math.ceil(totalPages);
			var start = Math.max(1, t.page() - 3);
			var end = Math.min(totalPages, t.page() + 3);
			return t.pages().filter(function(val){
				return val.get('index') >= start && val.get('index') < end;
			});
		},
		search: function(evt, ui){
			var t=this;
			evt.preventDefault();
			
			var q = $('form[role="search"] input[name="search"]').val();
			if(q !== t.query()){
				t.page(1);
				t.query(q);
				t.loadItems();
			}
			
			return false;
		},
		
		loadItems: function(){
			var t=this;
			var url = init.listUrl;
			var params = [];

			if(t.query() !== null && t.query() !== ''){
				params.push('q=' + t.query());
				t.page(1);
				//Trigger page change if query changes, since it's a different page
				t.trigger('change:page');
			}
			if(t.page() !== 1){
				params.push('page=' + t.page());
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
					var model = t.model();
					if(model === null || model === undefined){
						t.model( new exports.ProductQueryResults(data, {parse: true}) );
					}else{
						var result = new exports.ProductQueryResults(data, {parse: true});
						t.rows().reset([]);
						t.model().results(result.results());
						t.model().count(result.count());
						
						t.updateRows();
					}
					resolve();
				}).error(function(){
					reject();
				});
			});
		},
		//helper Filter functions
		notFirst: function(val){
			return val > 1;
		},
		notLast: function(val){
			var t=this;
			var totalPages = (t.model().count() - 1) / 20 + 1;
			return val < totalPages;
		},
		isCurrentPage: function(val){
			return val == this.page();
		}
		
	});
	
	exports.ProductRouter = mvvm.Router.extend({
		
	});
	
	return exports;
});