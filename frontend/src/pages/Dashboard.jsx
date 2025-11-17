import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { toast } from 'react-toastify';
import { dashboardAPI } from '../services/api';

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await dashboardAPI.getStats();
      setStats(response.data);
    } catch (error) {
      toast.error('Failed to fetch dashboard statistics');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (!stats) return null;

  const statCards = [
    {
      title: 'Total Employees',
      value: stats.total_employees,
      icon: 'E',
      color: 'from-blue-500 to-cyan-500',
      link: '/employees'
    },
    {
      title: 'Total Tasks',
      value: stats.total_tasks,
      icon: 'T',
      color: 'from-purple-500 to-pink-500',
      link: '/tasks'
    },
    {
      title: 'Upcoming Due',
      value: stats.upcoming_due_tasks,
      icon: 'U',
      color: 'from-yellow-500 to-orange-500',
      link: '/tasks'
    },
    {
      title: 'Overdue Tasks',
      value: stats.overdue_tasks,
      icon: 'O',
      color: 'from-red-500 to-rose-500',
      link: '/tasks'
    }
  ];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-2">
          Dashboard
        </h1>
        <p className="text-gray-600">Welcome back! Here's an overview of your organization.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((card, index) => (
          <Link
            key={index}
            to={card.link}
            className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 border border-gray-100"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 mb-1">{card.title}</p>
                <p className="text-3xl font-bold text-gray-900">{card.value}</p>
              </div>
              <div className={`w-16 h-16 rounded-full bg-gradient-to-br ${card.color} flex items-center justify-center text-white text-2xl font-bold shadow-lg`}>
                {card.icon}
              </div>
            </div>
          </Link>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Tasks by Status</h2>
          <div className="space-y-4">
            {Object.entries(stats.tasks_by_status || {}).map(([status, count]) => {
              const total = Object.values(stats.tasks_by_status).reduce((a, b) => a + b, 0);
              const percentage = total > 0 ? (count / total) * 100 : 0;
              const colors = {
                'Todo': 'bg-gray-400',
                'In Progress': 'bg-yellow-400',
                'Done': 'bg-green-400'
              };
              return (
                <div key={status}>
                  <div className="flex justify-between mb-1">
                    <span className="text-sm font-medium text-gray-700">{status}</span>
                    <span className="text-sm font-medium text-gray-900">{count}</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div
                      className={`h-2.5 rounded-full ${colors[status] || 'bg-gray-400'} transition-all duration-500`}
                      style={{ width: `${percentage}%` }}
                    ></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Tasks by Priority</h2>
          <div className="space-y-4">
            {Object.entries(stats.tasks_by_priority || {}).map(([priority, count]) => {
              const total = Object.values(stats.tasks_by_priority).reduce((a, b) => a + b, 0);
              const percentage = total > 0 ? (count / total) * 100 : 0;
              const colors = {
                'Low': 'bg-blue-400',
                'Medium': 'bg-yellow-400',
                'High': 'bg-orange-400',
                'Urgent': 'bg-red-400'
              };
              return (
                <div key={priority}>
                  <div className="flex justify-between mb-1">
                    <span className="text-sm font-medium text-gray-700">{priority}</span>
                    <span className="text-sm font-medium text-gray-900">{count}</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div
                      className={`h-2.5 rounded-full ${colors[priority] || 'bg-gray-400'} transition-all duration-500`}
                      style={{ width: `${percentage}%` }}
                    ></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Link
            to="/employees/add"
            className="flex items-center p-4 bg-gradient-to-r from-blue-50 to-cyan-50 rounded-lg hover:from-blue-100 hover:to-cyan-100 transition-all duration-200 border border-blue-200"
          >
            <div className="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center text-white mr-4">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
            </div>
            <div>
              <p className="font-semibold text-gray-900">Add New Employee</p>
              <p className="text-sm text-gray-600">Register a new team member</p>
            </div>
          </Link>
          <Link
            to="/tasks/add"
            className="flex items-center p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg hover:from-purple-100 hover:to-pink-100 transition-all duration-200 border border-purple-200"
          >
            <div className="w-10 h-10 rounded-full bg-purple-500 flex items-center justify-center text-white mr-4">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
            </div>
            <div>
              <p className="font-semibold text-gray-900">Create New Task</p>
              <p className="text-sm text-gray-600">Assign a task to an employee</p>
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;

