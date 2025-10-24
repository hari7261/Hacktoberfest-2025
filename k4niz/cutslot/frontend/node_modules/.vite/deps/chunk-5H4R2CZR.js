import {
  __esm,
  __export
} from "./chunk-V4OQ3NZ2.js";

// node_modules/@supabase/node-fetch/browser.js
var browser_exports = {};
__export(browser_exports, {
  Headers: () => Headers,
  Request: () => Request,
  Response: () => Response,
  default: () => browser_default,
  fetch: () => fetch
});
var getGlobal, globalObject, fetch, browser_default, Headers, Request, Response;
var init_browser = __esm({
  "node_modules/@supabase/node-fetch/browser.js"() {
    getGlobal = function() {
      if (typeof self !== "undefined") {
        return self;
      }
      if (typeof window !== "undefined") {
        return window;
      }
      if (typeof global !== "undefined") {
        return global;
      }
      throw new Error("unable to locate global object");
    };
    globalObject = getGlobal();
    fetch = globalObject.fetch;
    browser_default = globalObject.fetch.bind(globalObject);
    Headers = globalObject.Headers;
    Request = globalObject.Request;
    Response = globalObject.Response;
  }
});

export {
  fetch,
  browser_default,
  Headers,
  Request,
  Response,
  browser_exports,
  init_browser
};
//# sourceMappingURL=chunk-5H4R2CZR.js.map
