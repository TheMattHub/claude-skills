-- An HTML anchor such as <a id="g-term"></a> marks a link target that GitHub renders, even
-- inside a table cell, where Markdown has no syntax for one. Pandoc keeps it as raw HTML and the
-- Word and LaTeX writers drop it, so links to #g-term would lead nowhere. Turn it into an empty
-- span with that id, which both writers turn into a bookmark or a \label.
function Inlines(inlines)
  for i = #inlines - 1, 1, -1 do
    local open, close = inlines[i], inlines[i + 1]
    if open.t == 'RawInline' and open.format == 'html' and close.t == 'RawInline' and close.format == 'html'
        and close.text:match('^</a>$') then
      local id = open.text:match('^<a%s+id="([^"]+)"%s*>$') or open.text:match('^<a%s+name="([^"]+)"%s*>$')
      if id then
        inlines[i] = pandoc.Span({}, { id = id })
        inlines:remove(i + 1)
      end
    end
  end
  return inlines
end
