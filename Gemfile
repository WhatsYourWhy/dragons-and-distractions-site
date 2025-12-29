source "https://rubygems.org"

# GitHub Pages gem (includes Jekyll and many plugins)
gem "github-pages", group: :jekyll_plugins

# Additional plugins required by _config.yml that may not be in github-pages
gem "jekyll-optional-front-matter"
gem "jekyll-titles-from-headings"

# Windows and JRuby does not include zoneinfo files, so bundle the tzinfo-data gem
# and associated library.
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

# Performance-booster for watching directories on Windows
gem "wdm", "~> 0.1", :platforms => [:windows]

# Lock `http_parser.rb` gem to `v0.6.x` on JRuby builds since newer versions of the gem
# do not have a Java counterpart.
gem "http_parser.rb", "~> 0.6.0", :platforms => [:jruby]
