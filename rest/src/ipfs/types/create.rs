use std::fmt;

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct ItemData {
    tbom: serde_json::Value,
    jwt: String,
    public_key: String,
}

impl ItemData {
    pub fn new(tbom: serde_json::Value, jwt: String, public_key: String) -> Self {
        ItemData {
            tbom,
            jwt,
            public_key,
        }
    }
}

impl fmt::Display for ItemData {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(
            f,
            "{{ tbom: {}, jwt: {}, public_key: {} }}",
            self.tbom, self.jwt, self.public_key
        )
    }
}

pub struct Options {
    quiet: Option<bool>,
    quieter: Option<bool>,
    silent: Option<bool>,
    progress: Option<bool>,
    trickle: Option<bool>,
    only_hash: Option<bool>,
    wrap_with_directory: Option<bool>,
    chunker: Option<String>,
    raw_leaves: Option<bool>,
    nocopy: Option<bool>,
    fs_cache: Option<bool>,
    cid_version: Option<i32>,
    hash: Option<String>,
    inline: Option<bool>,
    inline_limit: Option<i32>,
    pin: Option<bool>,
    to_files: Option<String>,
    preserve_mode: Option<bool>,
    preserve_mtime: Option<bool>,
    mode: Option<u32>,
    mtime: Option<i64>,
    mtime_nsecs: Option<u32>,
}

#[allow(dead_code)]
impl Options {
    pub fn builder() -> OptionsBuilder {
        OptionsBuilder::new()
    }

    pub fn as_urlencode_tuple(&self) -> Vec<(String, String)> {
        let mut options = Vec::new();

        if let Some(quiet) = self.quiet {
            options.push(("quiet".to_string(), quiet.to_string()));
        }

        if let Some(quieter) = self.quieter {
            options.push(("quieter".to_string(), quieter.to_string()));
        }

        if let Some(silent) = self.silent {
            options.push(("silent".to_string(), silent.to_string()));
        }

        if let Some(progress) = self.progress {
            options.push(("progress".to_string(), progress.to_string()));
        }

        if let Some(trickle) = self.trickle {
            options.push(("trickle".to_string(), trickle.to_string()));
        }

        if let Some(only_hash) = self.only_hash {
            options.push(("only-hash".to_string(), only_hash.to_string()));
        }

        if let Some(wrap_with_directory) = self.wrap_with_directory {
            options.push((
                "wrap-with-directory".to_string(),
                wrap_with_directory.to_string(),
            ));
        }

        if let Some(chunker) = &self.chunker {
            options.push(("chunker".to_string(), chunker.to_string()));
        }

        if let Some(raw_leaves) = self.raw_leaves {
            options.push(("raw-leaves".to_string(), raw_leaves.to_string()));
        }

        if let Some(nocopy) = self.nocopy {
            options.push(("nocopy".to_string(), nocopy.to_string()));
        }

        if let Some(fs_cache) = self.fs_cache {
            options.push(("fs-cache".to_string(), fs_cache.to_string()));
        }

        if let Some(cid_version) = self.cid_version {
            options.push(("cid-version".to_string(), cid_version.to_string()));
        }

        if let Some(hash) = &self.hash {
            options.push(("hash".to_string(), hash.to_string()));
        }

        if let Some(inline) = self.inline {
            options.push(("inline".to_string(), inline.to_string()));
        }

        if let Some(inline_limit) = self.inline_limit {
            options.push(("inline-limit".to_string(), inline_limit.to_string()));
        }

        if let Some(pin) = self.pin {
            options.push(("pin".to_string(), pin.to_string()));
        }

        if let Some(to_files) = &self.to_files {
            options.push(("to-files".to_string(), to_files.to_string()));
        }

        if let Some(preserve_mode) = self.preserve_mode {
            options.push(("preserve-mode".to_string(), preserve_mode.to_string()));
        }

        if let Some(preserve_mtime) = self.preserve_mtime {
            options.push(("preserve-mtime".to_string(), preserve_mtime.to_string()));
        }

        if let Some(mode) = self.mode {
            options.push(("mode".to_string(), mode.to_string()));
        }

        if let Some(mtime) = self.mtime {
            options.push(("mtime".to_string(), mtime.to_string()));
        }

        if let Some(mtime_nsecs) = self.mtime_nsecs {
            options.push(("mtime-nsecs".to_string(), mtime_nsecs.to_string()));
        }

        options
    }
}

impl Default for Options {
    fn default() -> Self {
        Options {
            quiet: None,
            quieter: None,
            silent: None,
            progress: None,
            trickle: None,
            only_hash: None,
            wrap_with_directory: None,
            chunker: None,
            raw_leaves: None,
            nocopy: None,
            fs_cache: None,
            cid_version: None,
            hash: None,
            inline: None,
            inline_limit: None,
            pin: None,
            to_files: None,
            preserve_mode: None,
            preserve_mtime: None,
            mode: None,
            mtime: None,
            mtime_nsecs: None,
        }
    }
}

#[allow(dead_code)]
pub struct OptionsBuilder {
    quiet: Option<bool>,
    quieter: Option<bool>,
    silent: Option<bool>,
    progress: Option<bool>,
    trickle: Option<bool>,
    only_hash: Option<bool>,
    wrap_with_directory: Option<bool>,
    chunker: Option<String>,
    raw_leaves: Option<bool>,
    nocopy: Option<bool>,
    fs_cache: Option<bool>,
    cid_version: Option<i32>,
    hash: Option<String>,
    inline: Option<bool>,
    inline_limit: Option<i32>,
    pin: Option<bool>,
    to_files: Option<String>,
    preserve_mode: Option<bool>,
    preserve_mtime: Option<bool>,
    mode: Option<u32>,
    mtime: Option<i64>,
    mtime_nsecs: Option<u32>,
}

#[allow(dead_code)]
impl OptionsBuilder {
    pub fn new() -> OptionsBuilder {
        OptionsBuilder {
            quiet: None,
            quieter: None,
            silent: None,
            progress: None,
            trickle: None,
            only_hash: None,
            wrap_with_directory: None,
            chunker: None,
            raw_leaves: None,
            nocopy: None,
            fs_cache: None,
            cid_version: None,
            hash: None,
            inline: None,
            inline_limit: None,
            pin: None,
            to_files: None,
            preserve_mode: None,
            preserve_mtime: None,
            mode: None,
            mtime: None,
            mtime_nsecs: None,
        }
    }

    pub fn quiet(mut self, quiet: bool) -> OptionsBuilder {
        self.quiet = Some(quiet);
        self
    }

    pub fn quieter(mut self, quieter: bool) -> OptionsBuilder {
        self.quieter = Some(quieter);
        self
    }

    pub fn silent(mut self, silent: bool) -> OptionsBuilder {
        self.silent = Some(silent);
        self
    }

    pub fn progress(mut self, progress: bool) -> OptionsBuilder {
        self.progress = Some(progress);
        self
    }

    pub fn trickle(mut self, trickle: bool) -> OptionsBuilder {
        self.trickle = Some(trickle);
        self
    }

    pub fn only_hash(mut self, only_hash: bool) -> OptionsBuilder {
        self.only_hash = Some(only_hash);
        self
    }

    pub fn wrap_with_directory(mut self, wrap_with_directory: bool) -> OptionsBuilder {
        self.wrap_with_directory = Some(wrap_with_directory);
        self
    }

    pub fn chunker(mut self, chunker: String) -> OptionsBuilder {
        self.chunker = Some(chunker);
        self
    }

    pub fn raw_leaves(mut self, raw_leaves: bool) -> OptionsBuilder {
        self.raw_leaves = Some(raw_leaves);
        self
    }

    pub fn nocopy(mut self, nocopy: bool) -> OptionsBuilder {
        self.nocopy = Some(nocopy);
        self
    }

    pub fn fs_cache(mut self, fs_cache: bool) -> OptionsBuilder {
        self.fs_cache = Some(fs_cache);
        self
    }

    pub fn cid_version(mut self, cid_version: i32) -> OptionsBuilder {
        self.cid_version = Some(cid_version);
        self
    }

    pub fn hash(mut self, hash: String) -> OptionsBuilder {
        self.hash = Some(hash);
        self
    }

    pub fn inline(mut self, inline: bool) -> OptionsBuilder {
        self.inline = Some(inline);
        self
    }

    pub fn inline_limit(mut self, inline_limit: i32) -> OptionsBuilder {
        self.inline_limit = Some(inline_limit);
        self
    }

    pub fn pin(mut self, pin: bool) -> OptionsBuilder {
        self.pin = Some(pin);
        self
    }

    pub fn to_files(mut self, to_files: String) -> OptionsBuilder {
        self.to_files = Some(to_files);
        self
    }

    pub fn preserve_mode(mut self, preserve_mode: bool) -> OptionsBuilder {
        self.preserve_mode = Some(preserve_mode);
        self
    }

    pub fn preserve_mtime(mut self, preserve_mtime: bool) -> OptionsBuilder {
        self.preserve_mtime = Some(preserve_mtime);
        self
    }

    pub fn mode(mut self, mode: u32) -> OptionsBuilder {
        self.mode = Some(mode);
        self
    }

    pub fn mtime(mut self, mtime: i64) -> OptionsBuilder {
        self.mtime = Some(mtime);
        self
    }

    pub fn mtime_nsecs(mut self, mtime_nsecs: u32) -> OptionsBuilder {
        self.mtime_nsecs = Some(mtime_nsecs);
        self
    }

    pub fn build(self) -> Options {
        Options {
            quiet: self.quiet,
            quieter: self.quieter,
            silent: self.silent,
            progress: self.progress,
            trickle: self.trickle,
            only_hash: self.only_hash,
            wrap_with_directory: self.wrap_with_directory,
            chunker: self.chunker,
            raw_leaves: self.raw_leaves,
            nocopy: self.nocopy,
            fs_cache: self.fs_cache,
            cid_version: self.cid_version,
            hash: self.hash,
            inline: self.inline,
            inline_limit: self.inline_limit,
            pin: self.pin,
            to_files: self.to_files,
            preserve_mode: self.preserve_mode,
            preserve_mtime: self.preserve_mtime,
            mode: self.mode,
            mtime: self.mtime,
            mtime_nsecs: self.mtime_nsecs,
        }
    }
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct Response {
    #[serde(rename = "Bytes")]
    bytes: Option<i64>,
    #[serde(rename = "Hash")]
    hash: String,
    #[serde(rename = "Mode")]
    mode: Option<String>,
    #[serde(rename = "Mtime")]
    mtime: Option<i64>,
    #[serde(rename = "MtimeNsecs")]
    m_time_nsecs: Option<i32>,
    #[serde(rename = "Name")]
    name: String,
    #[serde(rename = "Size")]
    size: String,
}

impl Response {
    pub fn get_hash(&self) -> String {
        self.hash.clone()
    }
}

impl Default for Response {
    fn default() -> Self {
        Response {
            bytes: Some(0),
            hash: String::new(),
            mode: Some(String::new()),
            mtime: Some(0),
            m_time_nsecs: Some(0),
            name: String::new(),
            size: String::new(),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_options_builder_default() {
        let options = Options::builder().build();
        assert_eq!(options.quiet, None);
        assert_eq!(options.quieter, None);
        assert_eq!(options.silent, None);
        assert_eq!(options.progress, None);
        assert_eq!(options.trickle, None);
        assert_eq!(options.only_hash, None);
        assert_eq!(options.wrap_with_directory, None);
        assert_eq!(options.chunker, None);
        assert_eq!(options.raw_leaves, None);
        assert_eq!(options.nocopy, None);
        assert_eq!(options.fs_cache, None);
        assert_eq!(options.cid_version, None);
        assert_eq!(options.hash, None);
        assert_eq!(options.inline, None);
        assert_eq!(options.inline_limit, None);
        assert_eq!(options.pin, None);
        assert_eq!(options.to_files, None);
        assert_eq!(options.preserve_mode, None);
        assert_eq!(options.preserve_mtime, None);
        assert_eq!(options.mode, None);
        assert_eq!(options.mtime, None);
        assert_eq!(options.mtime_nsecs, None);
    }

    #[test]
    fn test_options_builder_with_values() {
        let options = Options::builder()
            .quiet(true)
            .quieter(false)
            .silent(true)
            .progress(false)
            .trickle(true)
            .only_hash(false)
            .wrap_with_directory(true)
            .chunker("size-262144".to_string())
            .raw_leaves(true)
            .nocopy(false)
            .fs_cache(true)
            .cid_version(1)
            .hash("sha2-256".to_string())
            .inline(true)
            .inline_limit(32)
            .pin(true)
            .to_files("/path/to/files".to_string())
            .preserve_mode(true)
            .preserve_mtime(false)
            .mode(0o755)
            .mtime(1627846261)
            .mtime_nsecs(123456789)
            .build();

        assert_eq!(options.quiet, Some(true));
        assert_eq!(options.quieter, Some(false));
        assert_eq!(options.silent, Some(true));
        assert_eq!(options.progress, Some(false));
        assert_eq!(options.trickle, Some(true));
        assert_eq!(options.only_hash, Some(false));
        assert_eq!(options.wrap_with_directory, Some(true));
        assert_eq!(options.chunker, Some("size-262144".to_string()));
        assert_eq!(options.raw_leaves, Some(true));
        assert_eq!(options.nocopy, Some(false));
        assert_eq!(options.fs_cache, Some(true));
        assert_eq!(options.cid_version, Some(1));
        assert_eq!(options.hash, Some("sha2-256".to_string()));
        assert_eq!(options.inline, Some(true));
        assert_eq!(options.inline_limit, Some(32));
        assert_eq!(options.pin, Some(true));
        assert_eq!(options.to_files, Some("/path/to/files".to_string()));
        assert_eq!(options.preserve_mode, Some(true));
        assert_eq!(options.preserve_mtime, Some(false));
        assert_eq!(options.mode, Some(0o755));
        assert_eq!(options.mtime, Some(1627846261));
        assert_eq!(options.mtime_nsecs, Some(123456789));
    }
}
