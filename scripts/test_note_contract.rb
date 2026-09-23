require 'minitest/autorun'
require 'tmpdir'
require_relative 'validate_notes'

class NoteContractTest < Minitest::Test
  VALID = "---\ntitle: A title\ndescription: A description\ndate: 2026-09-23\ntags: [memory]\n---\nAn article without prescribed sections.\n"
  def check(source, name = 'new-note.md')
    Dir.mktmpdir do |dir|
      path = Pathname.new(dir).join(name)
      path.write(source)
      validate_note(path)
    end
  end
  def test_valid_minimal_article
    assert_equal 'A title', check(VALID)['title']
  end
  def test_missing_or_empty_metadata
    %w[title description date tags].each do |key|
      assert_raises(RuntimeError, ArgumentError) { check(VALID.gsub(/^#{key}:.*\n/, '')) }
    end
    assert_raises(RuntimeError) { check(VALID.sub('title: A title', 'title: " "')) }
  end
  def test_duplicate_yaml_key
    assert_raises(RuntimeError) { check(VALID.sub('title: A title', "title: First\ntitle: Second")) }
  end
  def test_invalid_and_backwards_dates
    assert_raises(ArgumentError) { check(VALID.sub('2026-09-23', '2026-02-30')) }
    assert_raises(RuntimeError) { check(VALID.sub('tags:', "last_modified_at: 2020-01-01\ntags:")) }
  end
  def test_invalid_tags_and_slug
    assert_raises(RuntimeError) { check(VALID.sub('[memory]', 'memory')) }
    assert_raises(RuntimeError) { check(VALID, 'Bad Slug.md') }
  end
  def test_routing_layout_and_publication_overrides
    ['layout: null', 'permalink: /elsewhere/', 'draft: true', 'sitemap: false'].each do |field|
      assert_raises(RuntimeError) { check(VALID.sub('tags:', "#{field}\ntags:")) }
    end
  end
  def test_empty_body
    assert_raises(RuntimeError) { check(VALID.sub('An article without prescribed sections.', '')) }
  end
  def test_explicit_modification_date
    assert_equal Date.new(2026, 9, 24), check(VALID.sub('tags:', "last_modified_at: 2026-09-24\ntags:"))['last_modified_at']
  end
end
