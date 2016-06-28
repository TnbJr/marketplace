var gulp = require('gulp');
var watch = require('gulp-watch');
var minfiycss = require('gulp-minify-css');
var livereload = require('gulp-livereload');
var browserSync = require('browser-sync').create();
var exec = require('child_process').exec;


gulp.task('watch', function(){
	browserSync.init({
    notify: false,
    port: 8000,
    proxy: '127.0.0.1:8000',
  });
	gulp.watch('**/templates/*/*').on('change', browserSync.reload);
	// gulp.watch('**/templates/*/*').on('change', browserSync.reload);
});

// gulp.task('runserver', function() {
//   var proc = exec('python manage.py runserver')
// })

// gulp.task('browserSync', ['runserver'], function() {
//   browserSync.init({
//     notify: false,
//     port: 8000,
//     proxy: 'localhost:8000'
//   })
// });

gulp.task('default', ['watch']);