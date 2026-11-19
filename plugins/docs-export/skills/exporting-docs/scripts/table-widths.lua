-- Gives every table relative column widths, so cells wrap instead of running off the page.
-- Pandoc's gfm reader leaves pipe tables at their natural width, which overflows in LaTeX
-- and makes Word break single words.
local stringify = pandoc.utils.stringify

local PAGE_CHARS = 100 -- characters that fit across an A4 text block, for the wider of the Word and PDF fonts
local TEXT_CAP = 150 -- longest cell counted per column: high enough that a column of sentences gets clearly more room than one of names

function Table(t)
  local n = #t.colspecs
  local len, word = {}, {}
  for i = 1, n do len[i], word[i] = 1, 1 end

  local function scan(rows)
    for _, row in ipairs(rows) do
      for i, cell in ipairs(row.cells) do
        if i <= n then
          local text = stringify(cell.contents)
          len[i] = math.max(len[i], #text)
          -- A hyphen is a break point in both Word and LaTeX, so each part of a hyphenated name counts on its own.
          for w in text:gmatch('[^%s%-]+%-?') do word[i] = math.max(word[i], #w) end
        end
      end
    end
  end
  scan(t.head.rows)
  for _, body in ipairs(t.bodies) do scan(body.body) end

  -- Each column first gets room for its longest unbreakable word (a name or a path cannot wrap);
  -- the factor covers capitals and monospace, which run wider than average text.
  -- What is left of the page goes to the columns that have more text, capped so one long cell does not take it all.
  local floor, floors, want, wants = {}, 0, {}, 0
  for i = 1, n do
    floor[i] = math.ceil(word[i] * 1.25) + 1
    floors = floors + floor[i]
    want[i] = math.max(0, math.min(len[i], TEXT_CAP) - floor[i])
    wants = wants + want[i]
  end
  local extra = math.max(0, PAGE_CHARS - 2 * n - floors)
  local share, sum = {}, 0
  for i = 1, n do
    share[i] = floor[i] + (wants > 0 and extra * want[i] / wants or extra / n)
    sum = sum + share[i]
  end
  for i = 1, n do t.colspecs[i][2] = share[i] / sum end
  return t
end
