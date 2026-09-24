#!/usr/bin/env ruby
# Technical authoring contract. Does not score prose or prescribe article sections.
require 'yaml'
require 'date'
require 'pathname'

def validate_note(path)
  source = path.read
  raise 'start the file with YAML front matter (---)' unless source.lines.first&.strip == '---'
  lines = source.lines
  closing = (1...lines.length).find { |i| lines[i].strip == '---' }
  raise 'close YAML front matter with ---' unless closing
  yaml = lines[1...closing].join
  data = YAML.safe_load(yaml, permitted_classes: [Date, Time], aliases: false)
  raise 'front matter must be a mapping' unless data.is_a?(Hash)
  keys = Psych.parse(yaml).root.children.each_slice(2).map { |key, _| key.value }
  raise 'duplicate front-matter keys' unless keys.uniq == keys
  %w[title description].each do |key|
    raise "#{key} must be a nonempty text string" unless data[key].is_a?(String) && !data[key].strip.empty?
  end
  dates = {}
  %w[date last_modified_at].each do |key|
    next if key == 'last_modified_at' && !data.key?(key)
    value = data[key]
    raise "#{key} must use YYYY-MM-DD" unless value.is_a?(Date) || (value.is_a?(String) && value.match?(/\A\d{4}-\d{2}-\d{2}\z/))
    dates[key] = Date.iso8601(value.to_s)
  end
  raise 'last_modified_at cannot precede date' if dates['last_modified_at'] && dates['last_modified_at'] < dates['date']
  tags = data['tags']
  raise 'tags must be a nonempty list of nonempty strings' unless tags.is_a?(Array) && !tags.empty? && tags.all? { |t| t.is_a?(String) && !t.strip.empty? }
  raise 'filename must be a lowercase hyphenated slug ending in .md or .markdown' unless path.basename.to_s.match?(/\A[a-z0-9]+(?:-[a-z0-9]+)*\.(md|markdown)\z/)
  raise 'use the shared note layout; omit layout or set it to note' if data.key?('layout') && data['layout'] != 'note'
  %w[permalink published draft sitemap canonical_url].each do |key|
    raise "#{key} overrides the publication contract; keep unfinished drafts outside _notes and discuss route/indexing exceptions explicitly" if data.key?(key)
  end
  raise 'article body is empty' if lines[(closing + 1)..-1].join.strip.empty?
  data
end

def note_paths(root)
  paths = Dir[root.join('**/*').to_s].select { |name| File.file?(name) }
  paths.each do |name|
    path = Pathname.new(name)
    raise "#{name}: keep articles directly in _notes as .md or .markdown files" unless path.dirname == root && %w[.md .markdown].include?(path.extname)
  end
  paths
end

if $PROGRAM_NAME == __FILE__
  begin
    paths = ARGV.empty? ? note_paths(Pathname.new(File.expand_path('../_notes', __dir__))) : ARGV
  rescue StandardError => e
    warn e.message
    exit 1
  end
  errors = []
  slugs = {}
  paths.each do |name|
    begin
      path = Pathname.new(name)
      validate_note(path)
      slug = path.basename.sub_ext('').to_s
      raise "duplicate article URL with #{slugs[slug]}" if slugs.key?(slug)
      slugs[slug] = name
    rescue StandardError => e
      errors << "#{name}: #{e.message}"
    end
  end
  warn errors.join("\n") unless errors.empty?
  puts "Article contract: #{paths.length} note(s), #{errors.length} failure(s)."
  exit(errors.empty? ? 0 : 1)
end
