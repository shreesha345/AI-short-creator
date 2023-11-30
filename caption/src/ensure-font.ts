import { staticFile } from "remotion";

export const ensureFont = () => {
  if (typeof window !== 'undefined' && 'FontFace' in window) {
    const regularFont = new FontFace(
      'IBM Plex Sans',
      `url(https://fonts.gstatic.com/s/ibmplexsans/v14/zYX9KVElMYYaJe8bpLHnCwDKjQ76AIFsdP3pBms.woff2)`,
    );

    const boldFont = new FontFace(
      'boldfont',
      `url('${staticFile("bold.ttf")}') format('truetype')`,
    );

    return Promise.all([regularFont.load(), boldFont.load()]).then(() => {
      document.fonts.add(regularFont);
      document.fonts.add(boldFont);
    });
  }

  throw new Error('browser does not support FontFace');
};
