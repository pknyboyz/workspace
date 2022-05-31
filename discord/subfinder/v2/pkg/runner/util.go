package runner

import (
	"strings"

	"github.com/pkg/errors"
	"github.com/projectdiscovery/fileutil"
)

var (
	ErrEmptyInput = errors.New("empty data")
)

func loadFromFile(file string) ([]string, error) {
	chanItems, err := fileutil.ReadFile(file)
	if err != nil {
		return nil, err
	}
	var items []string
	for item := range chanItems {
		var err error
		item, err = sanitize(item)
		if errors.Is(err, ErrEmptyInput) {
			continue
		}
		items = append(items, item)
	}
	return items, nil
}

func sanitize(data string) (string, error) {
	data = strings.Trim(data, "\n\t\"' ")
	if data == "" {
		return "", ErrEmptyInput
	}
	return data, nil
}
