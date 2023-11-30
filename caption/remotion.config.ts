/**
 * Note: When using the Node.JS APIs, the config file
 * doesn't apply. Instead, pass options directly to the APIs.
 *
 * All configuration options: https://remotion.dev/docs/config
 */

import { Config } from '@remotion/cli/config';
// import { Config } from "@remotion/cli/config";
import { enableTailwind } from "@remotion/tailwind";
 
Config.overrideWebpackConfig((currentConfiguration) => {
  return enableTailwind(currentConfiguration);
});
Config.setVideoImageFormat('jpeg');
Config.setOverwriteOutput(true);

// This template processes the whole audio file on each thread which is heavy.
// You are safe to increase concurrency if the audio file is small or your machine strong!
Config.setConcurrency(1);
