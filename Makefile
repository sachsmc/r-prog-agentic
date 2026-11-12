# Every target is a thin wrapper around a uv command, so the same commands
# work on Windows without make. See README.md.
UV ?= uv

.PHONY: all course refs index test clean

all: course refs index test

# Rebuild course/ from the pinned course repo. Needs quarto and R.
course:
	$(UV) run build/convert_course.py

# Fetch the reference books at their pins and build refs/.
refs:
	$(UV) run build/fetch_refs.py

# Build the search index in .index/ from course/ and refs/.
index:
	$(UV) run build/build_index.py

# Unit tests and the retrieval evaluation.
test:
	$(UV) run --with pytest --with pyyaml --with numpy --with tokenizers pytest -q -s eval

clean:
	rm -rf refs .index .cache
