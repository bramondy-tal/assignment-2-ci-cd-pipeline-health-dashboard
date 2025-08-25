import React, { useState, useCallback } from 'react';
import api from './api';
import Card from './components/Card';
import BuildStatusPie from './components/BuildStatusPie';
import BranchDurationBar from './components/BranchDurationBar';
import LatestBuildsTable from './components/LatestBuildsTable';
import { STATUS_LABELS } from './constants';

export default function Dashboard() {
  // Step 1: Ingest Repository
  const [repo, setRepo] = useState('');
  const [branch, setBranch] = useState('');
  const [ingesting, setIngesting] = useState(false);
  const [ingestMsg, setIngestMsg] = useState('');
  const [step, setStep] = useState(1);

  // Step 2: Metrics
  const [metrics, setMetrics] = useState(null);
  const [pieData, setPieData] = useState([]);
  const [barData, setBarData] = useState([]);
  const [lastStatus, setLastStatus] = useState(null);
  const [builds, setBuilds] = useState([]);
  const [loading, setLoading] = useState(false);

  // Ingest repo/branch
  const handleIngest = async (e) => {
    e.preventDefault();
    setIngesting(true);
    setIngestMsg('');
    try {
      // Split repo into owner/repo
      const [owner, repoName] = repo.split('/');
      if (!owner || !repoName) {
        setIngestMsg('Repository must be in the format owner/repo');
        setIngesting(false);
        return;
      }
      await api.post('/ingest/github-actions', null, {
        params: { owner, repo: repoName, branch }
      });
      setIngestMsg('Repository connected successfully!');
      setStep(2);
      fetchMetrics();
    } catch (e) {
      setIngestMsg('Failed to connect repository');
    }
    setIngesting(false);
  };

  // Fetch metrics after ingestion
  const fetchMetrics = useCallback(async () => {
    setLoading(true);
    try {
      const [srRes, avgRes] = await Promise.all([
        api.get('/metrics/success-rate', { params: { repo, branch } }),
        api.get('/metrics/average-duration', { params: { repo, branch } }),
      ]);
      setMetrics(srRes.data);
      setPieData([
        { status: 'success', value: srRes.data.success_count || 0 },
        { status: 'failure', value: srRes.data.failure_count || 0 },
      ]);
      setBarData([{ branch: branch || 'All', avg_duration: avgRes.data.average_duration_seconds || 0, status: 'success' }]);
      // last-status may 404 if no builds; handle gracefully
      try {
        const lastRes = await api.get('/metrics/last-status', { params: { repo, branch } });
        setLastStatus(lastRes.data);
      } catch (err) {
        setLastStatus(null);
      }
      setBuilds([]);
    } catch (e) {
      // handle error
    }
    setLoading(false);
  }, [repo, branch]);

  // Helper functions
  const formatSeconds = (seconds) => {
    if (!seconds) return 'N/A';
    if (seconds < 60) return `${seconds}s`;
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}m ${secs}s`;
  };

  const formatDateTime = (dateTime) => {
    if (!dateTime) return 'N/A';
    return new Date(dateTime).toLocaleString();
  };

  // UI
  return (
    <div className="min-h-screen grid place-items-center bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900 text-white">
      {/* Step 1: Connect Repository */}
      {step === 1 && (
        <div className="flex items-center justify-center px-4 py-10 w-full">
          <div className="w-full max-w-4xl">
            <div className="text-center">
              <h1 className="text-5xl md:text-6xl lg:text-7xl font-extrabold mb-6 bg-gradient-to-r from-purple-300 via-pink-300 to-indigo-300 bg-clip-text text-transparent leading-tight">
                Connect Your Repository
              </h1>
              <p className="text-lg md:text-xl text-gray-200 mb-12 max-w-3xl mx-auto leading-relaxed">
                Seamlessly integrate your GitHub repository and monitor CI/CD pipeline performance with real-time insights and comprehensive analytics.
              </p>
            </div>

            <div className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-3xl shadow-2xl p-8 sm:p-10">
              <h3 className="text-xl md:text-2xl font-semibold mb-6 text-center text-gray-100">Repository Details</h3>
              <form className="flex flex-col md:flex-row items-stretch justify-center gap-4" onSubmit={handleIngest}>
                <input
                  className="flex-1 min-w-0 bg-white/10 border border-white/30 rounded-xl px-4 py-4 md:py-5 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent text-base md:text-lg"
                  placeholder="owner/repository"
                  value={repo}
                  onChange={e => setRepo(e.target.value)}
                  required
                />
                <input
                  className="flex-1 min-w-0 bg-white/10 border border-white/30 rounded-xl px-4 py-4 md:py-5 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent text-base md:text-lg"
                  placeholder="branch (e.g. main)"
                  value={branch}
                  onChange={e => setBranch(e.target.value)}
                  required
                />
                <button
                  type="submit"
                  className="whitespace-nowrap bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white px-6 md:px-8 lg:px-10 py-4 md:py-5 rounded-xl font-bold text-base md:text-lg transition-all duration-300 shadow-lg hover:shadow-2xl focus:outline-none focus:ring-2 focus:ring-purple-400 disabled:opacity-50"
                  disabled={ingesting}
                >
                  {ingesting ? 'Connecting…' : 'Connect'}
                </button>
              </form>
              {ingestMsg && (
                <div className="mt-6 text-center text-green-300 bg-green-500/20 border border-green-400/30 rounded-lg p-3">
                  {ingestMsg}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Step 2: Metrics Dashboard */}
      {step === 2 && (
        <div className="p-6 flex items-center justify-center w-full">
          <div className="w-full max-w-6xl mx-auto flex flex-col gap-8">
            {/* Header */}
            <div className="flex flex-col items-center text-center gap-2 mb-2">
              <h1 className="text-2xl sm:text-3xl md:text-4xl font-extrabold bg-gradient-to-r from-purple-200 via-pink-200 to-indigo-200 bg-clip-text text-transparent">Pipeline Overview</h1>
              <p className="text-sm sm:text-base text-gray-300">Repository: <span className="px-2 py-0.5 rounded-full bg-white/10 border border-white/20">{repo}</span> • Branch: <span className="px-2 py-0.5 rounded-full bg-white/10 border border-white/20">{branch}</span></p>
              <button
                onClick={() => setStep(1)}
                className="mt-2 bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg transition-colors"
              >Connect Another Repository</button>
            </div>

            {/* Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 place-items-center">
              {loading ? (
                <>
                  <div className="rounded-xl p-6 bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 animate-pulse h-24" />
                  <div className="rounded-xl p-6 bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 animate-pulse h-24" />
                  <div className="rounded-xl p-6 bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 animate-pulse h-24" />
                </>
              ) : (
                <>
                  <div className="w-full bg-white/5 hover:bg-white/10 transition-colors border border-white/10 hover:border-white/20 rounded-2xl p-6 text-center shadow-sm hover:shadow md:hover:-translate-y-1 md:transition-transform">
                    <div className="mx-auto mb-3 w-12 h-12 rounded-xl bg-gradient-to-br from-emerald-500 to-emerald-400 grid place-items-center text-2xl">✅</div>
                    <div className="text-3xl md:text-4xl font-extrabold text-emerald-300">{metrics ? `${Math.round((metrics.success_rate || 0) * 100)}%` : '-'}</div>
                    <div className="text-gray-300 text-sm md:text-base mt-1">Success Rate</div>
                  </div>
                  <div className="w-full bg-white/5 hover:bg-white/10 transition-colors border border-white/10 hover:border-white/20 rounded-2xl p-6 text-center shadow-sm hover:shadow md:hover:-translate-y-1 md:transition-transform">
                    <div className="mx-auto mb-3 w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-500 to-sky-500 grid place-items-center text-2xl">📈</div>
                    <div className="text-3xl md:text-4xl font-extrabold text-indigo-200">{metrics ? `${metrics.success_count || 0}` : '-'}</div>
                    <div className="text-gray-300 text-sm md:text-base mt-1">Successes</div>
                  </div>
                  <div className="w-full bg-white/5 hover:bg-white/10 transition-colors border border-white/10 hover:border-white/20 rounded-2xl p-6 text-center shadow-sm hover:shadow md:hover:-translate-y-1 md:transition-transform">
                    <div className="mx-auto mb-3 w-12 h-12 rounded-xl bg-gradient-to-br from-rose-500 to-orange-500 grid place-items-center text-2xl">⛔</div>
                    <div className="text-3xl md:text-4xl font-extrabold text-rose-200">{metrics ? `${metrics.failure_count || 0}` : '-'}</div>
                    <div className="text-gray-300 text-sm md:text-base mt-1">Failures</div>
                  </div>
                </>
              )}
            </div>

            {/* Insight chips */}
            {!loading && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="flex items-center gap-3 bg-white/5 border border-white/10 rounded-xl p-4">
                  <span className="inline-flex items-center justify-center w-8 h-8 rounded-lg bg-gradient-to-br from-violet-500 to-fuchsia-500 text-white">⏱️</span>
                  <div>
                    <div className="text-xs uppercase tracking-wide text-gray-300">Average Duration</div>
                    <div className="text-lg font-semibold">{formatSeconds(barData?.[0]?.avg_duration)}</div>
                  </div>
                </div>
                <div className="flex items-center gap-3 bg-white/5 border border-white/10 rounded-xl p-4">
                  <span className="inline-flex items-center justify-center w-8 h-8 rounded-lg bg-gradient-to-br from-amber-500 to-orange-500 text-white">🕒</span>
                  <div>
                    <div className="text-xs uppercase tracking-wide text-gray-300">Last Build</div>
                    <div className="text-lg font-semibold">{lastStatus ? (STATUS_LABELS[lastStatus.status] || lastStatus.status) : 'N/A'}</div>
                  </div>
                </div>
              </div>
            )}

            {/* Charts */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 place-items-center">
              {loading ? (
                <>
                  <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-6 h-72 animate-pulse" />
                  <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-6 h-72 animate-pulse" />
                </>
              ) : (
                <>
                  <div className="w-full bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-6">
                    <h2 className="text-lg font-semibold mb-4 flex items-center gap-2"><span>📊</span> Build Results</h2>
                    <BuildStatusPie data={pieData} />
                  </div>
                  <div className="w-full bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-6">
                    <div className="flex items-center justify-between mb-4">
                      <h2 className="text-lg font-semibold flex items-center gap-2"><span>⏱️</span> Average Build Duration</h2>
                      <span className="text-sm text-gray-300 bg-gray-700 px-3 py-1 rounded-full">{formatSeconds(barData?.[0]?.avg_duration)}</span>
                    </div>
                    <BranchDurationBar data={barData} />
                  </div>
                </>
              )}
            </div>

            {/* Last Build Status */}
            <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-6">
              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2"><span>🕒</span> Last Build Status</h2>
              {lastStatus ? (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-sm">
                  <div>
                    <div className="text-gray-400">Status</div>
                    <div className="text-xl font-bold">{STATUS_LABELS[lastStatus.status] || lastStatus.status}</div>
                  </div>
                  <div>
                    <div className="text-gray-400">Duration</div>
                    <div className="font-semibold">{formatSeconds(lastStatus.duration_seconds)}</div>
                  </div>
                  <div>
                    <div className="text-gray-400">Started</div>
                    <div className="font-semibold">{formatDateTime(lastStatus.started_at)}</div>
                  </div>
                  <div>
                    <div className="text-gray-400">Finished</div>
                    <div className="font-semibold">{formatDateTime(lastStatus.finished_at)}</div>
                  </div>
                </div>
              ) : (
                <div className="text-sm text-gray-400">No builds found yet for the selected repository and branch.</div>
              )}
            </div>

            {/* Latest Builds Table */}
            <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-6">
              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2"><span>📝</span> Latest Builds</h2>
              <div className="max-h-96 overflow-y-auto">
                {loading ? (
                  <div className="h-48 animate-pulse bg-gray-700/30 rounded" />
                ) : builds.length > 0 ? (
                  <LatestBuildsTable builds={builds} />
                ) : (
                  <div className="text-center py-8 text-gray-400">No builds data available yet.</div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
