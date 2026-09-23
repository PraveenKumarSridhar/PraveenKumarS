#!/usr/bin/env ruby
# Authoring preflight; GitHub Pages continues to use jekyll-seo-tag.
require 'yaml'
require 'date'
require 'pathname'

normalize = !!ARGV.delete('--normalize-empty')
root = Pathname.new(__dir__).parent.realpath
paths = ARGV.empty? ? Dir[root.join('_notes/*.{md,markdown}').to_s] : ARGV
errors = []
updates = []

paths.each do |name|
  path = Pathname.new(name).expand_path
  begin
    source = path.read
    lines = source.lines
    raise 'missing YAML front matter' unless lines.first&.strip == '---'
    closing = (1...lines.length).find { |i| lines[i].strip == '---' }
    raise 'unclosed YAML front matter' unless closing
    front_lines = lines[1...closing]
    front = front_lines.join
    data = YAML.safe_load(front, permitted_classes: [Date, Time], aliases: false)
    raise 'front matter must be a mapping' unless data.is_a?(Hash)
    node = Psych.parse(front).root
    pairs = node.children.each_slice(2).to_a
    raise 'duplicate top-level image keys' if pairs.count { |key, _| key.value == 'image' } > 1
    next unless data.key?('image')
    image = data['image']
    value = image.is_a?(Hash) ? image['path'] : image
    empty = value.nil? || (value.is_a?(String) && value.strip.empty?)
    if empty
      unless normalize
        raise 'empty image override; omit it or run with --normalize-empty'
      end
      raise 'cannot normalize flow-style front matter; omit the empty image manually' if node.style == Psych::Nodes::Mapping::FLOW
      # Use parser source positions to remove only this top-level field.
      index = pairs.index { |key, _| key.value == 'image' }
      first = pairs[index][0].start_line
      last = pairs[index + 1] ? pairs[index + 1][0].start_line : front_lines.length
      front_lines.slice!(first...last)
      begin
        rewritten = YAML.safe_load(front_lines.join, permitted_classes: [Date, Time], aliases: false)
      rescue Psych::Exception
        raise 'cannot safely normalize this image field; omit it manually (rewritten YAML is invalid)'
      end
      rewritten = {} if rewritten.nil?
      unless rewritten == data.reject { |key, _| key == 'image' }
        raise 'cannot safely normalize this image field; omit it manually (other metadata would change)'
      end
      updates << [path, lines[0] + front_lines.join + lines[closing..-1].join]
      next
    end
    raise 'image must be a path string or a mapping with a path string' unless value.is_a?(String)
    raise 'image path must not contain surrounding whitespace' unless value == value.strip
    raise 'use a root-relative local asset path for a verifiable social image' unless value.start_with?('/') && !value.start_with?('//')
    asset = root.join(value.sub(%r{\A/}, '')).cleanpath
    raise 'image path escapes the site directory' unless asset.to_s.start_with?(root.to_s + '/')
    raise "missing image asset: #{value}" unless asset.file?
  rescue StandardError => e
    errors << "#{name}: #{e.message}"
  end
end

unless errors.empty?
  warn errors.join("\n")
  exit 1
end
updates.each do |path, source|
  path.write(source)
  puts "Normalized empty image: #{path}"
end
puts "Validated #{paths.length} note(s); #{updates.length} empty override(s) normalized."
