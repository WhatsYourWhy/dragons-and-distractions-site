source "https://rubygems.org"

# Keep the existing Jekyll/Minima versions without the unused remote-theme
# downloader (github-pages pins jekyll-remote-theme to a vulnerable rubyzip).
gem "jekyll", "= 3.10.0"
gem "minima", "= 2.5.1"

# Plugins used by _config.yml
gem "jekyll-optional-front-matter"
gem "jekyll-sitemap"
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
