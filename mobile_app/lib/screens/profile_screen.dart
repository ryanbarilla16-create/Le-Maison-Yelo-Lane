import 'package:flutter/material.dart';
import '../theme.dart';
import '../services/api_service.dart';
import '../services/auth_service.dart';
import 'login_screen.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});
  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  Map<String, dynamic>? _user;
  bool _loading = true;
  bool _saving = false;
  String? _error;
  final _firstCtrl = TextEditingController();
  final _lastCtrl = TextEditingController();
  final _usernameCtrl = TextEditingController();
  final _emailCtrl = TextEditingController();
  final _phoneCtrl = TextEditingController();

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() {
      _loading = true;
      _error = null;
    });

    try {
      final userId = await AuthService.getUserId();
      if (userId == null) {
        if (!mounted) return;
        setState(() {
          _error = 'Not logged in. Please log in again.';
          _loading = false;
        });
        return;
      }

      final res = await ApiService.get('/api/user/$userId/profile');

      if (!mounted) return;

      if (res != null && res is Map<String, dynamic>) {
        setState(() {
          _user = res;
          _firstCtrl.text = res['first_name'] ?? '';
          _lastCtrl.text = res['last_name'] ?? '';
          _usernameCtrl.text = res['username'] ?? '';
          _emailCtrl.text = res['email'] ?? '';
          _phoneCtrl.text = res['phone_number'] ?? '';
          _loading = false;
        });
      } else {
        // API call failed or returned unexpected data — use local cached user data as fallback
        final cachedUser = await AuthService.getUser();
        if (!mounted) return;

        if (cachedUser != null) {
          setState(() {
            _user = cachedUser;
            _firstCtrl.text = cachedUser['first_name'] ?? '';
            _lastCtrl.text = cachedUser['last_name'] ?? '';
            _usernameCtrl.text = cachedUser['username'] ?? '';
            _emailCtrl.text = cachedUser['email'] ?? '';
            _phoneCtrl.text = cachedUser['phone_number'] ?? '';
            _loading = false;
          });
        } else {
          setState(() {
            _error =
                'Could not load profile.\nMake sure Flask is running and your device is on the same network.';
            _loading = false;
          });
        }
      }
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _error = 'Connection error: $e';
        _loading = false;
      });
    }
  }

  Future<void> _save() async {
    setState(() => _saving = true);
    final userId = await AuthService.getUserId();
    final res = await ApiService.put('/api/user/$userId/profile', {
      'first_name': _firstCtrl.text.trim(),
      'last_name': _lastCtrl.text.trim(),
      'username': _usernameCtrl.text.trim(),
      'email': _emailCtrl.text.trim(),
      'phone_number': _phoneCtrl.text.trim(),
    });
    setState(() => _saving = false);
    final ok = res['success'] == true;
    if (ok) {
      final u = await AuthService.getUser();
      if (u != null) {
        u['first_name'] = _firstCtrl.text.trim();
        u['last_name'] = _lastCtrl.text.trim();
        u['username'] = _usernameCtrl.text.trim();
        u['email'] = _emailCtrl.text.trim();
        u['phone_number'] = _phoneCtrl.text.trim();
        await AuthService.saveUser(u);
      }
    }
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(res['message'] ?? ''),
        backgroundColor: ok ? AppColors.success : AppColors.danger,
      ),
    );
  }

  Future<void> _logout() async {
    await AuthService.logout();
    if (!mounted) return;
    Navigator.pushAndRemoveUntil(
      context,
      MaterialPageRoute(builder: (_) => const LoginScreen()),
      (_) => false,
    );
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return const Center(
        child: CircularProgressIndicator(color: AppColors.primary),
      );
    }

    // Show error state with retry button
    if (_error != null) {
      return Scaffold(
        appBar: AppBar(
          title: Text(
            'Profile',
            style: AppTextStyles.heading.copyWith(fontSize: 20),
          ),
          centerTitle: true,
        ),
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(32),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  padding: const EdgeInsets.all(20),
                  decoration: BoxDecoration(
                    color: AppColors.danger.withOpacity(0.1),
                    shape: BoxShape.circle,
                  ),
                  child: const Icon(
                    Icons.person_off_rounded,
                    color: AppColors.danger,
                    size: 48,
                  ),
                ),
                const SizedBox(height: 20),
                Text(
                  'Profile Unavailable',
                  style: AppTextStyles.heading.copyWith(fontSize: 20),
                ),
                const SizedBox(height: 8),
                Text(
                  _error!,
                  textAlign: TextAlign.center,
                  style: AppTextStyles.muted.copyWith(fontSize: 13),
                ),
                const SizedBox(height: 24),
                ElevatedButton.icon(
                  onPressed: _load,
                  icon: const Icon(Icons.refresh),
                  label: const Text('Try Again'),
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 28,
                      vertical: 14,
                    ),
                  ),
                ),
                const SizedBox(height: 12),
                OutlinedButton.icon(
                  onPressed: _logout,
                  icon: const Icon(Icons.logout),
                  label: const Text('Sign Out'),
                  style: OutlinedButton.styleFrom(
                    foregroundColor: AppColors.danger,
                    side: const BorderSide(color: AppColors.danger),
                  ),
                ),
              ],
            ),
          ),
        ),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Profile',
          style: AppTextStyles.heading.copyWith(fontSize: 20),
        ),
        centerTitle: true,
      ),
      body: RefreshIndicator(
        color: AppColors.primary,
        onRefresh: _load,
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              // Avatar
              CircleAvatar(
                radius: 45,
                backgroundColor: AppColors.primary.withOpacity(0.1),
                backgroundImage: _user?['profile_picture_url'] != null
                    ? NetworkImage(_user!['profile_picture_url'])
                    : null,
                child: _user?['profile_picture_url'] == null
                    ? Text(
                        '${(_user?['first_name'] ?? 'U')[0]}',
                        style: const TextStyle(
                          fontSize: 32,
                          fontWeight: FontWeight.bold,
                          color: AppColors.primary,
                        ),
                      )
                    : null,
              ),
              const SizedBox(height: 12),
              Text(
                '${_user?['first_name'] ?? ''} ${_user?['last_name'] ?? ''}',
                style: AppTextStyles.heading.copyWith(fontSize: 20),
              ),
              Text('@${_user?['username'] ?? ''}', style: AppTextStyles.muted),
              const SizedBox(height: 24),
              _field('First Name', _firstCtrl, Icons.person_outline),
              _field('Last Name', _lastCtrl, Icons.person_outline),
              _field('Username', _usernameCtrl, Icons.alternate_email),
              _field('Email', _emailCtrl, Icons.email_outlined),
              _field('Phone', _phoneCtrl, Icons.phone_outlined),
              const SizedBox(height: 20),
              SizedBox(
                width: double.infinity,
                height: 52,
                child: ElevatedButton(
                  onPressed: _saving ? null : _save,
                  child: _saving
                      ? const SizedBox(
                          width: 22,
                          height: 22,
                          child: CircularProgressIndicator(
                            color: Colors.white,
                            strokeWidth: 2.5,
                          ),
                        )
                      : const Text('Save Changes'),
                ),
              ),
              const SizedBox(height: 12),
              SizedBox(
                width: double.infinity,
                height: 48,
                child: OutlinedButton.icon(
                  onPressed: _logout,
                  icon: const Icon(Icons.logout),
                  label: const Text('Sign Out'),
                  style: OutlinedButton.styleFrom(
                    foregroundColor: AppColors.danger,
                    side: const BorderSide(color: AppColors.danger),
                  ),
                ),
              ),
              const SizedBox(height: 30),
            ],
          ),
        ),
      ),
    );
  }

  Widget _field(String label, TextEditingController ctrl, IconData icon) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 14),
      child: TextField(
        controller: ctrl,
        decoration: InputDecoration(
          labelText: label,
          prefixIcon: Icon(icon, color: AppColors.primary),
        ),
      ),
    );
  }
}
