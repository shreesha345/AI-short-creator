import React from 'react';
import { SubtitleItem } from 'parse-srt';

export const Word: React.FC<{
  item: SubtitleItem;
  frame: number;
}> = ({ item, frame }) => {
  const words = item.text.split(' ').slice(0, 3).join(' ');

  return (
    <span>
      {words.toUpperCase()}
    </span>
  );
};
